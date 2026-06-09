from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainQuery, JackTrainResponse


class JackTrainRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: JackTrainQuery) -> JackTrainResponse:
        '''잭 도슨의 자기 소개 레포지토리 추상 메소드'''
        pass
