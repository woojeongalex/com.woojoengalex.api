"""[Layer: Ports] Walter 입력 Port — 승객 조회."""

from abc import ABC, abstractmethod

from titanic.app.dtos.walter_page import WalterPassengerPageDto


class WalterUseCase(ABC):
    @abstractmethod
    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageDto:
        pass
