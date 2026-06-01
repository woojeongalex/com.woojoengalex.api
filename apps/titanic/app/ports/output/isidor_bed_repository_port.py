"""[Layer: Ports] Isidor bed 출력 Port — 조회 계약."""

from abc import ABC, abstractmethod
from typing import Any


class IsidorBedRepositoryPort(ABC):
    @abstractmethod
    async def get_isidor_bed(self) -> dict[str, Any]:
        pass
