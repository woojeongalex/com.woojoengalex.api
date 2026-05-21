import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.models.evaluation_models import AiVocalAnalysisEvaluationEntity
from music.app.repositories.evaluation_repository import EvaluationRepository
from music.app.schemas.evaluation_schemas import (
    VocalEvaluationCreateRequest,
    VocalEvaluationResponse,
)

logger = logging.getLogger(__name__)


class EvaluationService:
    """3단계 AI 평가 스키마 순서대로 엔티티에 매핑 후 저장."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._repository = EvaluationRepository(db)

    async def save_evaluation(
        self, body: VocalEvaluationCreateRequest
    ) -> VocalEvaluationResponse:
        entity = AiVocalAnalysisEvaluationEntity(
            pitch_score=body.pitch_score,
            rhythm_score=body.rhythm_score,
            vocal_grade=body.vocal_grade,
            summary=body.summary,
            catalog_song_id=body.catalog_song_id,
            mr_search_list_id=body.mr_search_list_id,
            input_source=body.input_source,
            file_name=body.file_name or "",
            duration_sec=body.duration_sec,
        )
        saved = await self._repository.save_evaluation(entity)
        logger.info(
            "[MUSIC][evaluation][4/service] 저장 완료 id=%s pitch=%s rhythm=%s grade=%s",
            saved.id,
            saved.pitch_score,
            saved.rhythm_score,
            saved.vocal_grade,
        )
        return VocalEvaluationResponse(id=saved.id)
