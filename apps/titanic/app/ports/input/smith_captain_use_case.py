"""[Layer: Ports] Smith captain 입력 Port (inbound → usecase)."""

from abc import ABC, abstractmethod


class SmithCaptainUseCase(ABC):
    @abstractmethod
    async def get_smith_captain(self) -> None:
        pass
