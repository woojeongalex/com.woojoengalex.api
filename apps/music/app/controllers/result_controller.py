import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.schemas.result_schemas import (
    AiVocalAnalysisResultCreateRequest,
    AiVocalAnalysisResultResponse,
)
from music.app.services.result_service import ResultService

logger = logging.getLogger(__name__)


class ResultController:
    """AI 보컬 분석 결과 저장 — Service에 위임."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._service = ResultService(db)

    async def save_ai_analysis_result(
        self, body: AiVocalAnalysisResultCreateRequest
    ) -> AiVocalAnalysisResultResponse:
        logger.info(
            "[MUSIC][result][3/controller] → service.save_ai_analysis_result input=%s",
            body.input_source,
        )
        return await self._service.save_ai_analysis_result(body)
