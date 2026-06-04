"""[Layer: Use Cases] Walter 조회 Query DTO."""

from dataclasses import dataclass


@dataclass
class WalterQuery:
    id: int
    name: str
    memo: str
