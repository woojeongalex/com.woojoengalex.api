"""[Layer: Ports] Hartley violin 출력 Port — 조회 계약."""

from abc import ABC, abstractmethod
from typing import Any


class HartleyViolinRepositoryPort(ABC):
    @abstractmethod
    async def get_hartley_violin(self) -> dict[str, Any]:
        pass
