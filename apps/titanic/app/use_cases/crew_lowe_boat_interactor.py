"""[Layer: Use Cases] Lowe boat (LoweBoatUseCase 구현)."""

from dataclasses import asdict
from typing import Any

from titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository


class LoweBoatInteractor(LoweBoatUseCase):
    def __init__(self, repository: LoweBoatRepository) -> None:
        self._repository = repository

    async def introduce_myself(self) -> dict[str, Any]:
        query = LoweBoatQuery(id=5, name="해롤드 로우 (Harold Lowe)")
        response = await self._repository.introduce_myself(query)
        return asdict(response)
