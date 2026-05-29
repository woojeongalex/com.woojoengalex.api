"""[Layer: Ports] Walter 출력 Port — read 조회 계약."""

from abc import ABC, abstractmethod
from typing import Any


class WalterRepositoryPort(ABC):
    @abstractmethod
    async def read_passengers(
        source_file: str | None, page: int, page_size: int
    ) -> dict[str, Any]:
        pass
