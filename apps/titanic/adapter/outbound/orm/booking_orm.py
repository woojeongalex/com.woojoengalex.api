"""Neon `titanic_bookings` ORM — BookingCommand 매핑."""

from typing import Optional

from pydantic import ConfigDict
from sqlmodel import Field, SQLModel

from titanic.app.dtos.james_command import BookingCommand


class BookingOrm(SQLModel, table=True):
    __tablename__ = "titanic_bookings"

    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: int = Field(foreign_key="titanic_persons.id", index=True)
    pclass: str = Field(max_length=8)
    ticket: str = Field(max_length=64)
    fare: str = Field(max_length=32)
    cabin: str = Field(default="", max_length=64)
    embarked: str = Field(default="", max_length=8)

    @classmethod
    def from_command(cls, person_id: int, command: BookingCommand) -> "BookingOrm":
        return cls(
            person_id=person_id,
            pclass=command.pclass,
            ticket=command.ticket,
            fare=command.fare,
            cabin=command.cabin,
            embarked=command.embarked,
        )
