from abc import ABC, abstractmethod

from the_wire.app.dtos.contact_dto import (
    ContactResult,
    SaveContactCommand,
    SearchContactQuery,
    UploadContactsResult,
)


class ContactUseCase(ABC):
    @abstractmethod
    async def save(self, command: SaveContactCommand) -> ContactResult: ...

    @abstractmethod
    async def search(self, query: SearchContactQuery) -> list[ContactResult]: ...

    @abstractmethod
    async def upload(
        self, commands: list[SaveContactCommand]
    ) -> UploadContactsResult: ...

    @abstractmethod
    async def list_all(self) -> list[ContactResult]: ...
