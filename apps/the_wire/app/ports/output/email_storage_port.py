from abc import ABC, abstractmethod

from the_wire.app.dtos.email_dto import (
    EmailStorageCommand,
    EmailStorageResult,
    SentEmailResult,
)


class EmailStoragePort(ABC):
    @abstractmethod
    async def save(
        self, command: EmailStorageCommand, embedding: list[float]
    ) -> EmailStorageResult: ...

    @abstractmethod
    async def list_sent(self) -> list[SentEmailResult]: ...
