"""[Layer: Use Cases] Smith captain (SmithCaptainUseCase 구현)."""
from fastapi import Depends
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema, SmithCaptainSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case
from titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase


class SmithCaptainInteractor(SmithCaptainUseCase):
    def __init__(self, repository: SmithCaptainRepository) -> None:
        self._repository = repository

    async def chat(self, schema: ChatSchema,
                    jack: JackTrainerUseCase = Depends(get_jack_trainer_use_case),
                    rose: RoseModelUseCase = Depends(get_rose_model_use_case)
                    ) -> SmithCaptainResponse:
    
            
        return await self._repository.chat(schema.message)


    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        return await self._repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name,
        ))




