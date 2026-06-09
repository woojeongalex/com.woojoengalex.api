"""Neon `titanic_persons` ORM — PersonCommand 매핑."""

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel

from titanic.app.dtos.crew_james_command import PersonCommand


class RoseModelOrm(SQLModel, table=True):
    __tablename__ = "titanic_persons"

    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    source_file: str = Field(max_length=255, index=True)
    passenger_id: str = Field(max_length=32, index=True)
    survived: str = Field(max_length=8)
    name: str = Field(max_length=255)
    gender: str = Field(max_length=16)
    age: str = Field(max_length=32)
    sib_sp: str = Field(max_length=8)
    parch: str = Field(max_length=8)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
        ),
    )

    @classmethod
    def from_command(cls, source_file: str, command: PersonCommand) -> "PersonOrm":
        return cls(
            source_file=source_file,
            passenger_id=command.passenger_id,
            survived=command.survived,
            name=command.name,
            gender=command.gender,
            age=command.age,
            sib_sp=command.sib_sp,
            parch=command.parch,
        )
