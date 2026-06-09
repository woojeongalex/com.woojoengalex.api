"""James upload — `Titanic-Dataset.csv` 기준 Use Case Command DTO.

- HTTP(Pydantic)와 분리: `adapter/inbound/api/mappers/james_inbound_mapper.py`
- Neon 저장: `PersonCommand` → `person_orm`, `BookingCommand` → `booking_orm`
"""

__all__ = ["PERSON_COMMAND_FIELDS", "BookingCommand", "PersonCommand"]
from dataclasses import dataclass

from titanic.app.dtos.passenger_row import PassengerRowDto

# PersonCommand 필드 순서 = CSV snake_case (Titanic-Dataset.csv)
PERSON_COMMAND_FIELDS: tuple[str, ...] = (
    "passenger_id",
    "survived",
    "pclass",
    "name",
    "gender",
    "age",
    "sib_sp",
    "parch",
    "ticket",
    "fare",
    "cabin",
    "embarked",
)


@dataclass
class PersonCommand:
    """CSV 1행 = Person + Booking + Port(country 제외) 역정규화."""

    passenger_id: str
    survived: str
    pclass: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    ticket: str
    fare: str
    cabin: str
    embarked: str

    def to_passenger_row(self) -> PassengerRowDto:
        return PassengerRowDto(
            passenger_id=self.passenger_id,
            survived=self.survived,
            pclass=self.pclass,
            name=self.name,
            gender=self.gender,
            age=self.age,
            sib_sp=self.sib_sp,
            parch=self.parch,
            ticket=self.ticket,
            fare=self.fare,
            cabin=self.cabin,
            embarked=self.embarked,
        )


@dataclass
class BookingCommand:
    """Booking + Port(embarked만) — `Titanic-Dataset.csv`에 있는 컬럼만."""

    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass
class JamesResponse:
    answer: str
