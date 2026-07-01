from the_wire.app.dtos.contact_dto import (
    ContactResult,
    SaveContactCommand,
    SearchContactQuery,
)
from the_wire.app.ports.input.contact_use_case import ContactUseCase
from the_wire.app.ports.output.contact_repository_port import ContactRepositoryPort


class ContactInteractor(ContactUseCase):
    def __init__(self, repository: ContactRepositoryPort) -> None:
        self._repository = repository

    async def save(self, command: SaveContactCommand) -> ContactResult:
        return await self._repository.save(command)

    async def search(self, query: SearchContactQuery) -> list[ContactResult]:
        return await self._repository.search(query)
