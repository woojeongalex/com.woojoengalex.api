import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.schemas.suggest_schema import (
    VocalRecommendationCreateRequest,
    VocalRecommendationResponse,
)
from music.app.services.suggest_service import SuggestService

logger = logging.getLogger(__name__)


class SuggestController:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self._service = SuggestService(db)

    async def create_recommendation(
        self, body: VocalRecommendationCreateRequest
    ) -> VocalRecommendationResponse:
        logger.info(
            "[MUSIC][suggest][2/controller] → service vocalSingResultId=%s",
            body.vocal_sing_result_id,
        )
        return await self._service.create_from_saved_result(body)

    async def get_latest(
        self, vocal_sing_result_id: int
    ) -> VocalRecommendationResponse | None:
        return await self._service.get_latest(vocal_sing_result_id)
