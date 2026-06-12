from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

logger = logging.getLogger(__name__)


class SmithCaptainPgRepository(SmithCaptainRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        logger.info(f"[SmithCaptainPgRepository] introduce_myself 진입 | request_data={query}")
        return SmithCaptainResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )

    async def chat(self, message: str) -> SmithCaptainResponse:
        logger.info(f"[SmithCaptainPgRepository] chat 진입 | message={message}")
        return SmithCaptainResponse(id=0, name="스미스 선장", answer=f"[임시 응답] 질문을 받았습니다: {message}")