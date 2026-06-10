"""Neon `bookings` ORM — RoseModel 매핑."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.theone_base import Base


class RoseModelOrm(Base):
    __tablename__ = "titanic_bookings"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    person_id: Mapped[str] = mapped_column(Integer, ForeignKey("titanic_passengers.id"), index=True)
    pclass: Mapped[str] = mapped_column(String, nullable=True)
    ticket: Mapped[str] = mapped_column(String, nullable=True)
    fare: Mapped[str] = mapped_column(String, nullable=True)
    cabin: Mapped[str] = mapped_column(String, nullable=True)
    embarked: Mapped[str] = mapped_column(String, nullable=True)

    @classmethod
    def from_command(cls, person_id: int, command) -> "RoseModelOrm":
        return cls(
            person_id=person_id,
            pclass=command.pclass,
            ticket=command.ticket,
            fare=command.fare,
            cabin=command.cabin,
            embarked=command.embarked,
        )
