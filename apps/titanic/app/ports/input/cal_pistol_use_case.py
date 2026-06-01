"""[Layer: Ports] Cal pistol 입력 Port (inbound → usecase)."""

from abc import ABC, abstractmethod


class CalPistolUseCase(ABC):
    @abstractmethod
    async def get_cal_pistol(self) -> None:
        pass
