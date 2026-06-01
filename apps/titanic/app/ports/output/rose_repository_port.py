"""[Layer: Ports] Rose 출력 Port — 데이터셋 스키마 조회 계약."""

from abc import ABC, abstractmethod
from typing import Any


class RoseRepositoryPort(ABC):
    @abstractmethod
    async def read_titanic_schema(self) -> dict[str, Any]:
        pass
