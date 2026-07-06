from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from the_wire.adapter.outbound.repositories.watch_pg_repository import WatchPgRepository
from the_wire.app.ports.input.watch_use_case import WatchUseCase
from the_wire.app.ports.output.watch_repository_port import WatchRepositoryPort
from the_wire.app.use_cases.watch_interactor import WatchInteractor

try:
    from database import get_db
except ModuleNotFoundError:
    from apps.database import get_db


def get_watch_repository(
    db: AsyncSession = Depends(get_db),
) -> WatchRepositoryPort:
    return WatchPgRepository(session=db)


def get_watch_use_case(
    repository: WatchRepositoryPort = Depends(get_watch_repository),
) -> WatchUseCase:
    return WatchInteractor(repository=repository)
