from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from the_wire.adapter.outbound.repositories.inbox_pg_repository import InboxPgRepository
from the_wire.app.ports.input.inbox_use_case import InboxUseCase
from the_wire.app.ports.output.inbox_repository_port import InboxRepositoryPort
from the_wire.app.use_cases.inbox_interactor import InboxInteractor

try:
    from database import get_db
except ModuleNotFoundError:
    from apps.database import get_db


def get_inbox_repository(
    db: AsyncSession = Depends(get_db),
) -> InboxRepositoryPort:
    return InboxPgRepository(session=db)


def get_inbox_use_case(
    repository: InboxRepositoryPort = Depends(get_inbox_repository),
) -> InboxUseCase:
    return InboxInteractor(repository=repository)
