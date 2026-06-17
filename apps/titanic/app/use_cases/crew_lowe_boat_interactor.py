"""[Layer: Use Cases] Lowe boat (LoweBoatUseCase 구현)."""

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.output.crew_lowe_boat_port import LoweBoatPort


class LoweBoatInteractor(LoweBoatUseCase):
    def __init__(self, repository: LoweBoatPort) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
        return await self._repository.introduce_myself(LoweBoatQuery(
            id=schema.id,
            name=schema.name,
        ))
