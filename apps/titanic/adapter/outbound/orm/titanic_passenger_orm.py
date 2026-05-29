"""Neon `titanic_passengers` ORM."""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel

from titanic.app.dtos.passenger_row import PassengerRowDto


class TitanicPassengerOrm(SQLModel, table=True):
    __tablename__ = "titanic_passengers"

    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    source_file: str = Field(max_length=255, index=True)
    dataset_passenger_id: str = Field(max_length=32, index=True)
    survived: str = Field(max_length=8)
    pclass: str = Field(max_length=8)
    name: str = Field(max_length=255)
    gender: str = Field(max_length=16)
    age: str = Field(max_length=32)
    sib_sp: str = Field(max_length=8)
    parch: str = Field(max_length=8)
    ticket: str = Field(max_length=64)
    fare: str = Field(max_length=32)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )

    @classmethod
    def from_passenger_row(
        cls,
        source_file: str,
        passenger: PassengerRowDto,
    ) -> "TitanicPassengerOrm":
        return cls(
            source_file=source_file,
            dataset_passenger_id=passenger.passenger_id,
            survived=passenger.survived,
            pclass=passenger.pclass,
            name=passenger.name,
            gender=passenger.gender,
            age=passenger.age,
            sib_sp=passenger.sib_sp,
            parch=passenger.parch,
            ticket=passenger.ticket,
            fare=passenger.fare,
        )
