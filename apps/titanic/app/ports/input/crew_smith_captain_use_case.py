from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema, SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase


class SmithCaptainUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        pass

    @abstractmethod
    async def chat(
        self,
        schema: ChatSchema,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
    ) -> SmithCaptainResponse:
        '''사용자 자연어 입력을 받아 채팅 응답을 반환'''
        pass
