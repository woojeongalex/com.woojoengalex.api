from abc import ABC, abstractmethod

from the_wire.app.dtos.contact_dto import (
    ContactResult,
    SaveContactCommand,
    SearchContactQuery,
)


class ContactUseCase(ABC):
    @abstractmethod
    async def save(self, command: SaveContactCommand) -> ContactResult: ...

    @abstractmethod
    async def search(self, query: SearchContactQuery) -> list[ContactResult]: ...
