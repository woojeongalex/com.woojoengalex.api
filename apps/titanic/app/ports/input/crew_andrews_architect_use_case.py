from abc import ABC, abstractmethod
from typing import Any


class AndrewsArchitectUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self) -> dict[str, Any]:
        pass
