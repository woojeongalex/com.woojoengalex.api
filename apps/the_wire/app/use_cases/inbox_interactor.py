import logging

from the_wire.app.dtos.inbox_dto import InboxResult, ReceiveMailCommand
from the_wire.app.ports.input.inbox_use_case import InboxUseCase
from the_wire.app.ports.output.inbox_repository_port import InboxRepositoryPort

logger = logging.getLogger(__name__)


class InboxInteractor(InboxUseCase):
    def __init__(self, repository: InboxRepositoryPort) -> None:
        self.repository = repository

    async def receive(self, command: ReceiveMailCommand) -> InboxResult:
        logger.info("[InboxInteractor] receive | sender=%s", command.sender)
        return await self.repository.save(command)

    async def list_inbox(self) -> list[InboxResult]:
        logger.info("[InboxInteractor] list_inbox")
        return await self.repository.find_all()
