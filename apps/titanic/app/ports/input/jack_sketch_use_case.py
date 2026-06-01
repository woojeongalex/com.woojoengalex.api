"""[Layer: Ports] Jack sketch 입력 Port (inbound → usecase)."""

from abc import ABC, abstractmethod


class JackSketchUseCase(ABC):
    @abstractmethod
    async def get_jack_sketch(self) -> None:
        pass
