import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.models.result_models import AiVocalAnalysisResultEntity
from music.app.repositories.result_repository import ResultRepository
from music.app.schemas.result_schemas import (
    AiVocalAnalysisResultCreateRequest,
    AiVocalAnalysisResultResponse,
)

logger = logging.getLogger(__name__)


class ResultService:
    """3단계 AI 분석 결과 스키마 순서대로 엔티티에 매핑 후 저장."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._repository = ResultRepository(db)

    async def save_ai_analysis_result(
        self, body: AiVocalAnalysisResultCreateRequest
    ) -> AiVocalAnalysisResultResponse:
        # 요청 필드 순서: pitch → rhythm → grade → summary → MR·메타 (스키마와 동일)
        entity = AiVocalAnalysisResultEntity(
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
        saved = await self._repository.save_ai_analysis_result(entity)
        logger.info(
            "[MUSIC][result][4/service] 저장 완료 id=%s pitch=%s rhythm=%s grade=%s",
            saved.id,
            saved.pitch_score,
            saved.rhythm_score,
            saved.vocal_grade,
        )
        return AiVocalAnalysisResultResponse(id=saved.id)
