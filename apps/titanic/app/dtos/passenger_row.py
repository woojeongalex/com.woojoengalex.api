"""[Layer: Use Cases] 업로드 승객 1행 DTO — HTTP/ORM과 분리."""

from dataclasses import dataclass


@dataclass
class PassengerRowDto:
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
