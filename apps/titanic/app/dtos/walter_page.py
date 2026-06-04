"""[Layer: Use Cases] Walter 조회 DTO."""

from dataclasses import dataclass
from typing import Any


@dataclass
class WalterPassengerPageDto:
    source_file: str | None
    page: int
    size: int
    total: int
    total_pages: int
    rows: list[dict[str, Any]]
