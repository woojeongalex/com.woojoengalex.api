import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.schemas.sing_schema import SingResultCreateRequest, SingResultResponse
from music.app.services.sing_service import SingService

logger = logging.getLogger(__name__)


class SingController:
    """보컬 분석 결과 저장 — Service에 위임."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._service = SingService(db)

    async def save_sing_result(self, body: SingResultCreateRequest) -> SingResultResponse:
        logger.info(
            "[MUSIC][sing][2/controller] → service.save_sing_result input=%s",
            body.input_source,
        )
        return await self._service.save_sing_result(body)
