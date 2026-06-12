from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse


class JackTrainerUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, request: Any) -> JackTrainerResponse:
        pass
