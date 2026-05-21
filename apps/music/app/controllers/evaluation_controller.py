import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.schemas.evaluation_schemas import (
    VocalEvaluationCreateRequest,
    VocalEvaluationResponse,
)
from music.app.services.evaluation_service import EvaluationService

logger = logging.getLogger(__name__)


class EvaluationController:
    """보컬 평가 저장 — Service에 위임."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._service = EvaluationService(db)

    async def save_evaluation(
        self, body: VocalEvaluationCreateRequest
    ) -> VocalEvaluationResponse:
        logger.info(
            "[MUSIC][evaluation][3/controller] → service.save_evaluation input=%s",
            body.input_source,
        )
        return await self._service.save_evaluation(body)
