"""[Layer: Ports] Ruth corset 출력 Port — 조회 계약."""

from abc import ABC, abstractmethod
from typing import Any


class RuthCorsetRepositoryPort(ABC):
    @abstractmethod
    async def get_ruth_corset(self) -> dict[str, Any]:
        pass
