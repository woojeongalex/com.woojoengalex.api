from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_walter_schema import WalterSchema
from titanic.app.dtos.crew_walter_query import WalterPassengerPageDto, WalterResponse


class WalterUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: WalterSchema) -> WalterResponse:
        pass

    @abstractmethod
    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageDto:
        pass
