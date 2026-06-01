"""[Layer: Ports] Hartley violin 입력 Port (inbound → usecase)."""

from abc import ABC, abstractmethod


class HartleyViolinUseCase(ABC):
    @abstractmethod
    async def get_hartley_violin(self) -> None:
        pass
