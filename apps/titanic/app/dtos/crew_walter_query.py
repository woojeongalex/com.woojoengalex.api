"""[Layer: Use Cases] Walter 조회 DTO."""

from dataclasses import dataclass
from typing import Any


@dataclass
class WalterQuery:
    id: int
    name: str
    memo: str


@dataclass
class WalterResponse:
    id: int
    name: str
    memo: str


@dataclass
class WalterPassengerPageDto:
    source_file: str | None
    page: int
    size: int
    total: int
    total_pages: int
    rows: list[dict[str, Any]]
