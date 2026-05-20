from sqlalchemy.ext.asyncio import AsyncSession

from music.app.schemas.sing_schema import SingResultCreateRequest, SingResultResponse
from music.app.services.result_service import ResultService


class SingService:
    """기존 호환 — 저장은 `ResultService`(result 레이어)에 위임."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._result = ResultService(db)

    async def save_sing_result(self, body: SingResultCreateRequest) -> SingResultResponse:
        return await self._result.save_ai_analysis_result(body)
