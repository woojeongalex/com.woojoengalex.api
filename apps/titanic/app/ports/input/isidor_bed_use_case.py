"""[Layer: Ports] Isidor bed 입력 Port (inbound → usecase)."""

from abc import ABC, abstractmethod


class IsidorBedUseCase(ABC):
    @abstractmethod
    async def get_isidor_bed(self) -> None:
        pass
