from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from the_wire.adapter.outbound.repositories.contact_pg_repository import (
    ContactPgRepository,
)
from the_wire.adapter.outbound.repositories.smtp_gateway import SmtpGateway
from the_wire.app.ports.input.contact_use_case import ContactUseCase
from the_wire.app.ports.input.email_use_case import EmailUseCase
from the_wire.app.ports.output.contact_repository_port import ContactRepositoryPort
from the_wire.app.ports.output.n8n_gateway_port import N8nGatewayPort
from the_wire.app.use_cases.contact_interactor import ContactInteractor
from the_wire.app.use_cases.email_interactor import EmailInteractor

from core.lol.t1_mid_faker_orchestrator import FakerOrchestrator

try:
    from database import get_db
except ModuleNotFoundError:
    from apps.database import get_db

_orchestrator = FakerOrchestrator()


def get_gateway() -> N8nGatewayPort:
    return SmtpGateway()


def get_email_use_case(
    gateway: N8nGatewayPort = Depends(get_gateway),
) -> EmailUseCase:
    return EmailInteractor(gateway=gateway, orchestrator=_orchestrator)


def get_contact_repository(
    db: AsyncSession = Depends(get_db),
) -> ContactRepositoryPort:
    return ContactPgRepository(session=db)


def get_contact_use_case(
    repository: ContactRepositoryPort = Depends(get_contact_repository),
) -> ContactUseCase:
    return ContactInteractor(repository=repository)
