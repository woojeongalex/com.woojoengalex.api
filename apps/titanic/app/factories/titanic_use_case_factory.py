"""[Layer: Application] Titanic Use Case 팩토리 추상."""

from abc import ABC, abstractmethod
from typing import Type

from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.input.walter_use_case import WalterUseCase


class TitanicUseCaseFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_james_use_case() -> Type[JamesUseCase]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_walter_use_case() -> Type[WalterUseCase]:
        raise NotImplementedError
