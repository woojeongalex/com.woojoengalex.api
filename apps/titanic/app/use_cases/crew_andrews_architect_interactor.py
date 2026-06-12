from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository


class AndrewsArchitectInteractor(AndrewsArchitectUseCase):
    def __init__(self, repository: AndrewsArchitectRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, request) -> AndrewsArchitectResponse:
        return await self._repository.introduce_myself(AndrewsArchitectQuery(
            id=request.id,
            name=request.name,
        ))
