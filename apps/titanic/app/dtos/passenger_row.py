"""[Layer: Use Cases] 업로드 승객 1행 DTO — HTTP/ORM과 분리."""

from dataclasses import dataclass, field


@dataclass
class PassengerRowDto:
    passenger_id: str | None = field(default=None)
    survived: str | None = field(default=None)
    pclass: str | None = field(default=None)
    name: str | None = field(default=None)
    gender: str | None = field(default=None)
    age: str | None = field(default=None)
    sib_sp: str | None = field(default=None)
    parch: str | None = field(default=None)
    ticket: str | None = field(default=None)
    fare: str | None = field(default=None)
    cabin: str | None = field(default=None)
    embarked: str | None = field(default=None)
