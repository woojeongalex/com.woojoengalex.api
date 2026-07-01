import asyncio
import logging

from the_wire.adapter.outbound.repositories.telegram_gateway import TelegramGateway
from the_wire.app.dtos.email_dto import EmailCommand, EmailResult
from the_wire.app.ports.input.email_use_case import EmailUseCase
from the_wire.app.ports.output.n8n_gateway_port import N8nGatewayPort

from core.lol.t1_mid_faker_orchestrator import FakerOrchestrator

logger = logging.getLogger(__name__)

_telegram = TelegramGateway()


class EmailInteractor(EmailUseCase):
    def __init__(
        self, gateway: N8nGatewayPort, orchestrator: FakerOrchestrator
    ) -> None:
        self._gateway = gateway
        self._orchestrator = orchestrator

    _PROMPT_TEMPLATE = (
        "반드시 한국어로 답해줘. "
        "실제 데이터가 없어도 괜찮으니 창의적으로 상상해서 답해줘. "
        "추가 질문 없이 바로 답변만 해줘.\n\n{topic}"
    )

    async def send_email(self, command: EmailCommand) -> EmailResult:
        prompt = self._PROMPT_TEMPLATE.format(topic=command.topic)
        body = await asyncio.to_thread(self._orchestrator.invoke, prompt)
        result = await self._gateway.send(command, body)
        if result.success:
            await _telegram.report(
                f"✅ <b>[The Wire 업무보고]</b>\n"
                f"수신자: <b>{command.to}</b> 에게\n"
                f"제목: {command.subject}\n"
                f"메일을 정상적으로 발송했습니다."
            )
        return result
