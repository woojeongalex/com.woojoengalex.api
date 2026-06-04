"""[Layer: Ports] Walter 출력 Port — 승객 조회."""

from abc import ABC, abstractmethod

from titanic.app.dtos.walter_page import WalterPassengerPageDto


class WalterRepositoryPort(ABC):
    @staticmethod
    @abstractmethod
    async def read_passengers(
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageDto:
        pass
