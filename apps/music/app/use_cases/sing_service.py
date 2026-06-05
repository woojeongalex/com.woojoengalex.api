from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.inbound.api.mappers.music_inbound_mapper import (
    from_evaluation_create,
    to_evaluation_response,
)
from music.adapter.inbound.api.schemas.sing_schema import (
    SingEvaluationCreateRequest,
    SingEvaluationResponse,
)
from music.adapter.outbound.pg.evaluation_pg_repository import EvaluationPgRepository
from music.adapter.outbound.pg.list_pg_repository import ListPgRepository
from music.app.use_cases.evaluation_interactor import EvaluationInteractor


class SingService:
    """호환 — 저장은 `EvaluationInteractor`에 위임."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        if db is None:
            raise RuntimeError("DB session is not available.")
        self._evaluation = EvaluationInteractor(
            repository=EvaluationPgRepository(session=db),
            list_repository=ListPgRepository(session=db),
        )

    async def save_sing_evaluation(
        self, body: SingEvaluationCreateRequest
    ) -> SingEvaluationResponse:
        result = await self._evaluation.upload(from_evaluation_create(body))
        return to_evaluation_response(result)
