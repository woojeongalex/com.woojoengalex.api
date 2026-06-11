from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema, SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase


class SmithCaptainUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장이 자신의 정보를 소개하는 메서드입니다.'''
        pass

    @abstractmethod
    async def chat(self, schema: ChatSchema,
                    jack: JackTrainUseCase,
                    rose: RoseModelUseCase
                    ) -> SmithCaptainResponse:
        ''''사용자가 채팅창에 입력한 자연어를 받아서 스미스 선장이 대답하는 메서드입니다.'''
        pass
