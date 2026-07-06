import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from the_wire.adapter.outbound.orm.email_model import EmailModel
from the_wire.app.dtos.email_dto import (
    EmailStorageCommand,
    EmailStorageResult,
    SentEmailResult,
)
from the_wire.app.ports.output.email_storage_port import EmailStoragePort

logger = logging.getLogger(__name__)


class EmailPgRepository(EmailStoragePort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(
        self, command: EmailStorageCommand, embedding: list[float]
    ) -> EmailStorageResult:
        model = EmailModel(
            recipient=command.to,
            subject=command.subject,
            body=command.body,
            embedding=embedding,
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        logger.info(
            "[EmailPgRepository] 저장 완료 | id=%s recipient=%s",
            model.id,
            model.recipient,
        )
        return EmailStorageResult(id=model.id)

    async def list_sent(self) -> list[SentEmailResult]:
        stmt = select(EmailModel).order_by(EmailModel.sent_at.desc()).limit(50)
        result = await self._session.execute(stmt)
        return [
            SentEmailResult(
                id=row.id,
                recipient=row.recipient,
                subject=row.subject,
                body=row.body,
                sent_at=row.sent_at.isoformat(),
                has_embedding=row.embedding is not None,
            )
            for row in result.scalars()
        ]
