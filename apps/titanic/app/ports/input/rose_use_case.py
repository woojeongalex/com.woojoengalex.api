"""[Layer: Ports] Rose 입력 Port — 데이터셋 스키마 (inbound → usecase)."""

from abc import ABC, abstractmethod


class RoseUseCase(ABC):
    @abstractmethod
    def read_titanic_schema(self) -> None:
        pass
