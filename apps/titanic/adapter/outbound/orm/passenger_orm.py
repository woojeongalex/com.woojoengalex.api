"""Neon `titanic_persons` ORM — PersonCommand 매핑."""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PersonOrm(Base):
    __tablename__ = "titanic_persons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_file: Mapped[str] = mapped_column(String(255), nullable=False)
    passenger_id: Mapped[str] = mapped_column(String(32), nullable=False)
    survived: Mapped[str] = mapped_column(String(8), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    gender: Mapped[str] = mapped_column(String(16), nullable=False)
    age: Mapped[str] = mapped_column(String(32), nullable=False)
    sib_sp: Mapped[str] = mapped_column(String(8), nullable=False)
    parch: Mapped[str] = mapped_column(String(8), nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
