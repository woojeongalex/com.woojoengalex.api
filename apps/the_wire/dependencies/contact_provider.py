from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from the_wire.adapter.outbound.repositories.contact_pg_repository import (
    ContactPgRepository,
)
from the_wire.app.ports.input.contact_use_case import ContactUseCase
from the_wire.app.ports.output.contact_repository_port import ContactRepositoryPort
from the_wire.app.use_cases.contact_interactor import ContactInteractor

try:
    from database import get_db
except ModuleNotFoundError:
    from apps.database import get_db


def get_contact_repository(
    db: AsyncSession = Depends(get_db),
) -> ContactRepositoryPort:
    return ContactPgRepository(session=db)


def get_contact_use_case(
    repository: ContactRepositoryPort = Depends(get_contact_repository),
) -> ContactUseCase:
    return ContactInteractor(repository=repository)
