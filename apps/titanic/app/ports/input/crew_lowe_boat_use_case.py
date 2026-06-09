from abc import ABC, abstractmethod
from typing import Any


class LoweBoatUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self) -> dict[str, Any]:
        pass
