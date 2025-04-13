import uuid

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import ORMBase

class RentalModel(ORMBase):
    __tablename__ = "rentals"

    id: Mapped[str] = mapped_column(
        Integer,
        autoincrement=True,
        primary_key=True  # This is crucial
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )
    book_id: Mapped[int] = mapped_column(
        nullable=False
    )

    user: Mapped["UserModel"] = relationship(back_populates='rentals')

