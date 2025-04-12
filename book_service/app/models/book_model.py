import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ORMBase


class BookModel(ORMBase):
    __tablename__ = "books"

    book_id: Mapped[uuid.UUID] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(nullable=False)
    available_copies: Mapped[int] = mapped_column(nullable=False, default=0)
