import asyncio
import logging

import google.generativeai as genai
import numpy as np
from the_wire.app.dtos.inbox_dto import InboxResult, ReceiveMailCommand
from the_wire.app.ports.input.inbox_use_case import InboxUseCase
from the_wire.app.ports.output.inbox_repository_port import InboxRepositoryPort

logger = logging.getLogger(__name__)

_EMBED_MODEL = "models/gemini-embedding-001"


class InboxInteractor(InboxUseCase):
    def __init__(self, repository: InboxRepositoryPort) -> None:
        self.repository = repository

    async def receive(self, command: ReceiveMailCommand) -> InboxResult:
        logger.info("[InboxInteractor] receive | sender=%s", command.sender)
        embedding = await self._generate_embedding(command)
        return await self.repository.save(command, embedding)

    async def _generate_embedding(
        self, command: ReceiveMailCommand
    ) -> np.ndarray | None:
        try:
            text = f"{command.subject}\n{command.body}"
            response = await asyncio.to_thread(
                genai.embed_content,
                model=_EMBED_MODEL,
                content=text,
                task_type="retrieval_document",
            )
            return np.array(response["embedding"], dtype=np.float32)
        except Exception:
            logger.exception("[InboxInteractor] 임베딩 생성 실패 — 저장은 계속 진행")
            return None

    async def list_inbox(self) -> list[InboxResult]:
        logger.info("[InboxInteractor] list_inbox")
        return await self.repository.find_all()
