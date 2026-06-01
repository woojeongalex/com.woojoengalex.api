"""[Layer: Ports] Ruth corset 입력 Port (inbound → usecase)."""

from abc import ABC, abstractmethod


class RuthCorsetUseCase(ABC):
    @abstractmethod
    async def get_ruth_corset(self) -> None:
        pass
