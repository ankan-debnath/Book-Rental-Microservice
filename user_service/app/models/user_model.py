import sqlite3
import uuid
from time import sleep

import sqlalchemy.exc
from sqlalchemy import String
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from typing import List

from .rental_model import RentalModel
from .base import ORMBase
from ..common.db import session_maker
from ..exceptions.custom_exceptions import UserNotFoundException
from ..schemas.user import CreateUserRequest, GetUserRequest, UpdateUserRequest, UserSchema


class UserModel(ORMBase):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda : str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    rentals: Mapped[List["RentalModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

async def create_user(session: AsyncSession, user: CreateUserRequest):
    new_user = UserModel(**user.model_dump())
    session.add(new_user)

    try:
        await session.commit()
        await session.refresh(new_user)
    except IntegrityError as e:
        await session.rollback()
        raise

    return new_user

async def if_user_exists(session: AsyncSession, user: CreateUserRequest):
    statement = select(UserModel).where(UserModel.email == user.email )
    existing = await session.scalar(statement)

    return existing

async def if_user_id_exists(session: AsyncSession, user_id: uuid.UUID) -> UserModel | None:
    statement = select(UserModel).where(UserModel.user_id == str(user_id))
    try:
        result = await session.execute(statement)
        user = result.scalars().first()
        if not user:
            return None
        await session.commit()
        await session.refresh(user)
        return user
    except sqlite3.OperationalError:
        await session.rollback()
        raise

async def get_user(session: AsyncSession, user_id: uuid.UUID) -> UserModel | None:
    statement = (
        select(UserModel)
        .where(UserModel.user_id == str(user_id))
        .options(selectinload(UserModel.rentals))  # Eager load rentals
    )
    try:
        result = await session.execute(statement)
        user = result.scalars().first()
        if not user:
            return None
        await session.commit()
        await session.refresh(user)
        return user

    except sqlalchemy.exc.OperationalError:
        raise

async def update_user(session: AsyncSession, user_id: uuid.UUID,  update_details:  dict):
    statement = (
        update(UserModel)
        .where(UserModel.user_id == str(user_id))
        .values(**update_details)
        .returning(UserModel)
    )

    try:
        result = await session.execute(statement)
        updated_user = result.scalars().first()

        if not updated_user:
            return None

        await session.commit()
        await session.refresh(updated_user)

    except sqlite3.IntegrityError:
        await session.rollback()
        raise
    except sqlite3.OperationalError:
        await session.rollback()
        raise

    return updated_user

async def delete_user(session: AsyncSession, user_id: uuid.UUID) -> UserModel | None:
    statement = (
        delete(UserModel)
        .where(UserModel.user_id == str(user_id))
        .returning(UserModel)
    )


    try:
        deleted_user = await session.scalar(statement)
        if not deleted_user:
            return None

        await session.commit()

    except sqlite3.OperationalError:
        await session.rollback()
        raise

    return deleted_user

async def rent_book(db: AsyncSession, user_id: uuid.UUID, book_id: uuid.UUID, copies: int) -> bool:
    statement = (
        select(UserModel)
        .options(selectinload(UserModel.rentals))
        .where(UserModel.user_id == str(user_id))
    )


    try:
        result = await db.execute(statement)
        user = result.scalars().first()
        if not user:
            return False

        for i in range(copies):
            new_rental = RentalModel(book_id=str(book_id))
            user.rentals.append(new_rental)

        await db.commit()
        return True

    except sqlite3.OperationalError:
        await db.rollback()
        raise

async def return_book(db: AsyncSession, user_id: uuid.UUID, book_id: uuid.UUID, copies: int) -> bool:
    try:
        result = await db.execute(
            select(UserModel)
            .options(selectinload(UserModel.rentals))
            .where(UserModel.user_id == str(user_id))
        )
        user = result.scalars().first()

        matching_rentals = [r for r in user.rentals if r.book_id == str(book_id)]
        for rental in matching_rentals[:copies]:
            await db.delete(rental)

        await db.commit()

        return True
    except sqlite3.OperationalError:
        await db.rollback()
        raise

async def if_user_email_exists(db: AsyncSession, email: str) -> UserModel | None:
    statement = (
        select(UserModel)
        .where(UserModel.email == email)
    )

    try:
        result = await db.execute(statement)
        user = result.scalars().first()

        if not user:
            return None
        await db.commit()
        await db.refresh(user)
        return user
    except sqlite3.OperationalError:
        await db.rollback()
        raise

async def get_user_rentals(db: AsyncSession, user_id: uuid.UUID) -> List[RentalModel] | None:
    statement = (
        select(UserModel)
        .options(selectinload(UserModel.rentals))
        .where(UserModel.user_id == str(user_id))
    )

    try:
        result = await db.execute(statement)
        user = result.scalars().first()
        if user:
            return user.rentals
        return None
    except sqlite3.OperationalError:
        raise




async def get_rental_details(db: AsyncSession, user_id: uuid.UUID) ->  Mapped[list[RentalModel]]:
    try:
        result = await db.execute(
            select(UserModel)
            .options(selectinload(UserModel.rentals))
            .where(UserModel.user_id == str(user_id))
        )
        user = result.scalars().first()

        rentals = user.rentals

        await db.commit()
        await db.refresh(user)

        for r in rentals:
            await db.refresh(r)

        return rentals

    except sqlite3.OperationalError:
        await db.rollback()
        raise

