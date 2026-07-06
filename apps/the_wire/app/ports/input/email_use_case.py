from abc import ABC, abstractmethod

from the_wire.app.dtos.email_dto import EmailCommand, EmailResult, SentEmailResult


class EmailUseCase(ABC):
    @abstractmethod
    async def send_email(self, command: EmailCommand) -> EmailResult: ...

    @abstractmethod
    async def list_sent(self) -> list[SentEmailResult]: ...
