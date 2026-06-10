from titanic.adapter.inbound.api.schemas.crew_walter_schema import WalterSchema
from titanic.app.dtos.crew_walter_query import WalterPassengerPageDto, WalterQuery, WalterResponse
from titanic.app.ports.input.crew_walter_use_case import WalterUseCase
from titanic.app.ports.output.crew_walter_director_repository import WalterDirectorRepository


class WalterInteractor(WalterUseCase):

    def __init__(self, repository: WalterDirectorRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: WalterSchema) -> WalterResponse:
        return await self._repository.introduce_myself(WalterQuery(
            id=schema.id,
            name=schema.name,
        ))

    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageDto:
        return await self._repository.read_passengers(source_file, page, size)