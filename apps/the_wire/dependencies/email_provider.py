from fastapi import Depends
from the_wire.adapter.outbound.repositories.smtp_gateway import SmtpGateway
from the_wire.app.ports.input.email_use_case import EmailUseCase
from the_wire.app.ports.output.n8n_gateway_port import N8nGatewayPort
from the_wire.app.use_cases.email_interactor import EmailInteractor

from core.lol.t1_mid_faker_orchestrator import FakerOrchestrator

_orchestrator = FakerOrchestrator()


def get_email_gateway() -> N8nGatewayPort:
    return SmtpGateway()


def get_email_use_case(
    gateway: N8nGatewayPort = Depends(get_email_gateway),
) -> EmailUseCase:
    return EmailInteractor(gateway=gateway, orchestrator=_orchestrator)
