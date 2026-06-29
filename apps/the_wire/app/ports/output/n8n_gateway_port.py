from abc import ABC, abstractmethod

from the_wire.app.dtos.email_dto import EmailCommand, EmailResult


class N8nGatewayPort(ABC):
    @abstractmethod
    async def send(self, command: EmailCommand, body: str) -> EmailResult: ...
