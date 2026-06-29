"""Neon `titanic_passengers` ORM — PersonCommand 매핑."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.theone_base import Base


class PersonOrm(Base):
    __tablename__ = "titanic_passengers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_file: Mapped[str | None] = mapped_column(String(255), nullable=True)
    passenger_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    survived: Mapped[str | None] = mapped_column(String(8), nullable=True)
    pclass: Mapped[str | None] = mapped_column(String(8), nullable=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(16), nullable=True)
    age: Mapped[str | None] = mapped_column(String(32), nullable=True)
    sib_sp: Mapped[str | None] = mapped_column(String(8), nullable=True)
    parch: Mapped[str | None] = mapped_column(String(8), nullable=True)
    ticket: Mapped[str | None] = mapped_column(String(64), nullable=True)
    fare: Mapped[str | None] = mapped_column(String(32), nullable=True)
    cabin: Mapped[str | None] = mapped_column(String(64), nullable=True)
    embarked: Mapped[str | None] = mapped_column(String(8), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
