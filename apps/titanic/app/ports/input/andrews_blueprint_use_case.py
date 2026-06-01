"""[Layer: Ports] Andrews blueprint 입력 Port (inbound → usecase)."""

from abc import ABC, abstractmethod


class AndrewsBlueprintUseCase(ABC):
    @abstractmethod
    async def get_andrews_blueprint(self) -> None:
        pass
