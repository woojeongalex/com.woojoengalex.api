from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse


class JackTrainerUseCase(ABC):

    @abstractmethod
    async def analyze_message_intent(self, user_message: str) -> dict:
        pass

    @abstractmethod
    async def introduce_myself(self, request: Any) -> JackTrainerResponse:
        pass

    @abstractmethod
    async def get_model_train(self) -> dict[str, Any]:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''
    