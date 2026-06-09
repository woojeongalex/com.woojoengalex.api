"""[Layer: Use Cases] Andrews architect (AndrewsArchitectUseCase 구현)."""

from dataclasses import asdict
from typing import Any

from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository


class AndrewsArchitectInteractor(AndrewsArchitectUseCase):
    def __init__(self, repository: AndrewsArchitectRepository) -> None:
        self._repository = repository

    async def introduce_myself(self) -> dict[str, Any]:
        query = AndrewsArchitectQuery(id=4, name="토마스 앤드류스 (Thomas Andrews)")
        response = await self._repository.introduce_myself(query)
        return asdict(response)
