import sqlite3
import uuid

import sqlalchemy.exc
from sqlalchemy import String
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


from .base import ORMBase
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

async def get_user(session: AsyncSession, user_id: uuid.UUID) -> UserModel | None:
    try:
        statement = select(UserModel).where(UserModel.user_id == str(user_id))
        user = await session.scalar(statement)

    except sqlalchemy.exc.OperationalError:
        raise
    return user

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
