from abc import ABC, abstractmethod

from the_wire.app.dtos.inbox_dto import InboxResult, ReceiveMailCommand


class InboxRepositoryPort(ABC):
    @abstractmethod
    async def save(self, command: ReceiveMailCommand) -> InboxResult: ...

    @abstractmethod
    async def find_all(self) -> list[InboxResult]: ...
