from datetime import datetime
import logging

import numpy as np
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from the_wire.adapter.outbound.orm.inbox_model import InboxModel
from the_wire.app.dtos.inbox_dto import InboxResult, ReceiveMailCommand
from the_wire.app.ports.output.inbox_repository_port import InboxRepositoryPort

logger = logging.getLogger(__name__)


def _to_result(m: InboxModel) -> InboxResult:
    return InboxResult(
        id=m.id,
        sender=m.sender,
        subject=m.subject,
        body=m.body,
        received_at=m.received_at,
        is_read=m.is_read,
    )


class InboxPgRepository(InboxRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(
        self, command: ReceiveMailCommand, embedding: np.ndarray | None = None
    ) -> InboxResult:
        logger.info("[InboxPgRepository] save | sender=%s", command.sender)
        mail = InboxModel(
            sender=command.sender,
            subject=command.subject,
            body=command.body,
            received_at=datetime.utcnow(),
            embedding=embedding,
        )
        self.session.add(mail)
        await self.session.commit()
        await self.session.refresh(mail)
        return _to_result(mail)

    async def find_all(self) -> list[InboxResult]:
        result = await self.session.execute(
            select(InboxModel).order_by(InboxModel.received_at.desc())
        )
        return [_to_result(m) for m in result.scalars().all()]
