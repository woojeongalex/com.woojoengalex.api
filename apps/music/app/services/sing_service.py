from sqlalchemy.ext.asyncio import AsyncSession

from music.app.schemas.sing_schema import SingEvaluationCreateRequest, SingEvaluationResponse
from music.app.services.evaluation_service import EvaluationService


class SingService:
    """호환 — 저장은 `EvaluationService`에 위임."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._evaluation = EvaluationService(db)

    async def save_sing_evaluation(
        self, body: SingEvaluationCreateRequest
    ) -> SingEvaluationResponse:
        return await self._evaluation.save_evaluation(body)
