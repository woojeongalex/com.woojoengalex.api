"""[Layer: Use Cases] Walter 조회 페이지 DTO."""

from dataclasses import dataclass


@dataclass(frozen=True)
class WalterPassengerItemDto:
    id: int
    source_file: str
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
    created_at: str | None = None


@dataclass(frozen=True)
class WalterPassengerPageDto:
    source_file: str | None
    page: int
    size: int
    total: int
    total_pages: int
    rows: tuple[WalterPassengerItemDto, ...]
