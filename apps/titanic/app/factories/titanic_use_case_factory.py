"""[Layer: Use Cases] Abstract Factory — James·Walter 패밀리 생성."""

from abc import ABC, abstractmethod
from typing import Type

from titanic.app.use_cases.james_command import JamesCommandImpl
from titanic.app.use_cases.walter_query import WalterQueryImpl


class TitanicUseCaseFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_james_use_case() -> Type[JamesCommandImpl]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_walter_use_case() -> Type[WalterQueryImpl]:
        raise NotImplementedError
