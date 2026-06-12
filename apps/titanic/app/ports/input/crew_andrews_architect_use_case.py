from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectResponse


class AndrewsArchitectUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, request: Any) -> AndrewsArchitectResponse:
        pass
