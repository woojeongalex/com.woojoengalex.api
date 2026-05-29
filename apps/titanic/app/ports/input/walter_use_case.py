"""[Layer: Ports] Walter 입력 Port — read 만 (inbound → usecase)."""

from abc import ABC, abstractmethod
from typing import Any


class WalterUseCase(ABC):
    @abstractmethod
    async def read_passengers(
        source_file: str | None, page: int, page_size: int
    ) -> dict[str, Any]:
        pass
