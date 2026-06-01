"""[Layer: Ports] Cal pistol 출력 Port — 조회 계약."""

from abc import ABC, abstractmethod
from typing import Any


class CalPistolRepositoryPort(ABC):
    @abstractmethod
    async def get_cal_pistol(self) -> dict[str, Any]:
        pass
