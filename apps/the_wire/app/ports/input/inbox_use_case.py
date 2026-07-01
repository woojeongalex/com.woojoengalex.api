from abc import ABC, abstractmethod

from the_wire.app.dtos.inbox_dto import InboxResult, ReceiveMailCommand


class InboxUseCase(ABC):
    @abstractmethod
    async def receive(self, command: ReceiveMailCommand) -> InboxResult: ...

    @abstractmethod
    async def list_inbox(self) -> list[InboxResult]: ...
