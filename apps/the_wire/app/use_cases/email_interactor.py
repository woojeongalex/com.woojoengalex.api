import asyncio
import logging

import google.generativeai as genai
import numpy as np
from the_wire.adapter.outbound.repositories.telegram_gateway import TelegramGateway
from the_wire.app.dtos.email_dto import (
    EmailCommand,
    EmailResult,
    EmailStorageCommand,
    SentEmailResult,
)
from the_wire.app.ports.input.email_use_case import EmailUseCase
from the_wire.app.ports.output.email_storage_port import EmailStoragePort
from the_wire.app.ports.output.n8n_gateway_port import N8nGatewayPort

from core.lol.t1_mid_faker_orchestrator import FakerOrchestrator

logger = logging.getLogger(__name__)

_telegram = TelegramGateway()

_EMBED_MODEL = "models/gemini-embedding-001"


class EmailInteractor(EmailUseCase):
    def __init__(
        self,
        gateway: N8nGatewayPort,
        orchestrator: FakerOrchestrator,
        storage: EmailStoragePort,
    ) -> None:
        self._gateway = gateway
        self._orchestrator = orchestrator
        self._storage = storage

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
            await self._save_with_embedding(command, body)

        return result

    async def _save_with_embedding(self, command: EmailCommand, body: str) -> None:
        try:
            text = f"{command.subject}\n{body}"
            response = await asyncio.to_thread(
                genai.embed_content,
                model=_EMBED_MODEL,
                content=text,
                task_type="retrieval_document",
            )
            embedding = np.array(response["embedding"], dtype=np.float32)
            storage_command = EmailStorageCommand(
                to=command.to,
                subject=command.subject,
                body=body,
            )
            await self._storage.save(storage_command, embedding)
            logger.info(
                "[EmailInteractor] pgvector 저장 완료 | recipient=%s", command.to
            )
        except Exception:
            logger.exception(
                "[EmailInteractor] pgvector 저장 실패 — 발송 결과에는 영향 없음"
            )

    async def list_sent(self) -> list[SentEmailResult]:
        return await self._storage.list_sent()
