"""[Layer: Ports] Andrews blueprint 출력 Port — 조회 계약."""

from abc import ABC, abstractmethod
from typing import Any


class AndrewsBlueprintRepositoryPort(ABC):
    @abstractmethod
    async def get_andrews_blueprint(self) -> dict[str, Any]:
        pass
