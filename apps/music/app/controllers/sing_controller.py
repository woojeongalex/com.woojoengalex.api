import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.schemas.sing_schema import SingEvaluationCreateRequest, SingEvaluationResponse
from music.app.services.sing_service import SingService

logger = logging.getLogger(__name__)


class SingController:
    """보컬 평가 저장 — Service에 위임."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._service = SingService(db)

    async def save_sing_evaluation(
        self, body: SingEvaluationCreateRequest
    ) -> SingEvaluationResponse:
        logger.info(
            "[MUSIC][sing][2/controller] → service.save_sing_evaluation input=%s",
            body.input_source,
        )
        return await self._service.save_sing_evaluation(body)
