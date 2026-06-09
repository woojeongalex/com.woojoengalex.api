from abc import ABC, abstractmethod

from titanic.app.dtos.crew_walter_query import WalterPassengerPageDto


class WalterDirectorRepository(ABC):
    @abstractmethod
    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageDto:
        pass
