"""[Layer: Ports] Smith captain 출력 Port — 조회 계약."""

from abc import ABC, abstractmethod
from typing import Any


class SmithCaptainRepositoryPort(ABC):
    @abstractmethod
    async def get_smith_captain(self) -> dict[str, Any]:
        pass
