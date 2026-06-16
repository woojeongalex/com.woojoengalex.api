from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse


class PredictionStrategy(Protocol):
    def predict(self, keywords: list[str]) -> float: ...


class RoseModelUseCase(ABC):

    @abstractmethod
    async def predict(self, keywords: list[str]) -> float:
        pass

    @abstractmethod
    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        pass
