from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.crew_walter_query import WalterPassengerPageDto


class WalterUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self) -> dict[str, Any]:
        pass

    @abstractmethod
    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageDto:
        pass
