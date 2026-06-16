from abc import ABC, abstractmethod

from titanic.app.dtos.crew_walter_query import WalterPassengerPageDto, WalterQuery, WalterResponse


class WalterDirectorRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: WalterQuery) -> WalterResponse:
        pass

    @abstractmethod
    async def get_train_set(self) -> WalterResponse:
        pass

    @abstractmethod
    async def get_test_set(self) -> WalterResponse:
        pass

    @abstractmethod
    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageDto:
        pass
