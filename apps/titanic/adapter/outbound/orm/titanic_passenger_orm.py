"""Neon `titanic_passengers` ORM — 업로드 CSV 1행 = 1레코드."""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from sqlalchemy import Column, DateTime, String, func
from sqlmodel import Field, SQLModel

from titanic.adapter.inbound.api.schemas.titanic_request import TitanicCommandRequest


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
    def from_command(
        cls,
        source_file: str,
        command: TitanicCommandRequest,
    ) -> "TitanicPassengerOrm":
        return cls(
            source_file=source_file,
            dataset_passenger_id=command.passenger_id,
            survived=command.survived,
            pclass=command.pclass,
            name=command.name,
            gender=command.gender,
            age=command.age,
            sib_sp=command.sib_sp,
            parch=command.parch,
            ticket=command.ticket,
            fare=command.fare,
        )
