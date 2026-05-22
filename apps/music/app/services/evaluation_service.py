import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.models.ai_vocal_analysis_model import AiVocalAnalysisEntity
from music.app.models.evaluation_models import SingEvaluationEntity
from music.app.models.user_vocal_recording_model import UserVocalRecordingEntity
from music.app.repositories.evaluation_repository import EvaluationRepository
from music.app.repositories.list_repository import ListRepository
from music.app.schemas.evaluation_schemas import (
    VocalEvaluationCreateRequest,
    VocalEvaluationResponse,
)

logger = logging.getLogger(__name__)


class EvaluationService:
    """3단계 AI 평가 스키마 순서대로 엔티티에 매핑 후 저장."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._repository = EvaluationRepository(db)
        self._list_repository = ListRepository(db)

    async def _resolve_catalog_and_mr(
        self,
        catalog_song_id: str | None,
        mr_search_list_id: int | None,
    ) -> tuple[str | None, int | None]:
        """MR이 있으면 catalog_song_id는 MR 행 기준으로 고정(이중 기록 불일치 방지)."""
        if mr_search_list_id is None:
            return catalog_song_id, None

        mr = await self._list_repository.get_by_id(mr_search_list_id)
        if mr is None:
            raise ValueError("선택한 MR 검색 기록을 찾을 수 없습니다.")

        resolved_catalog = mr.catalog_song_id
        if (
            catalog_song_id is not None
            and catalog_song_id != resolved_catalog
        ):
            logger.warning(
                "[MUSIC][evaluation][4/service] catalogSongId=%s → MR 기준 %s 로 정정",
                catalog_song_id,
                resolved_catalog,
            )
        return resolved_catalog, mr_search_list_id

    async def save_evaluation(
        self, body: VocalEvaluationCreateRequest
    ) -> VocalEvaluationResponse:
        catalog_song_id, mr_search_list_id = await self._resolve_catalog_and_mr(
            body.catalog_song_id,
            body.mr_search_list_id,
        )

        engine = "librosa" if body.input_source == "video" else "mic_demo"

        file_name = body.file_name or ""
        # 로그인 연동 후 API에서 user_id 전달 시 세션·녹음 행에 동일 값 설정
        user_id: int | None = None

        evaluation = SingEvaluationEntity(
            user_id=user_id,
            catalog_song_id=catalog_song_id,
            mr_search_list_id=mr_search_list_id,
            input_source=body.input_source,
            pitch_score=body.pitch_score,
            rhythm_score=body.rhythm_score,
            vocal_grade=body.vocal_grade,
            summary=body.summary,
            file_name=file_name,
            duration_sec=body.duration_sec,
        )
        vocal_recording = UserVocalRecordingEntity(
            sing_evaluation_id=0,
            user_id=user_id,
            catalog_song_id=catalog_song_id,
            mr_search_list_id=mr_search_list_id,
            input_source=body.input_source,
            file_name=file_name,
            duration_sec=body.duration_sec,
        )
        ai_analysis = AiVocalAnalysisEntity(
            user_vocal_recording_id=0,
            analysis_engine=engine,
            pitch_score=body.pitch_score,
            rhythm_score=body.rhythm_score,
            vocal_grade=body.vocal_grade,
            summary=body.summary,
        )
        saved_eval, saved_rec, saved_ai = await self._repository.save_evaluation_bundle(
            evaluation, vocal_recording, ai_analysis
        )
        logger.info(
            "[MUSIC][evaluation][4/service] 저장 완료 eval=%s recording=%s ai=%s",
            saved_eval.id,
            saved_rec.id,
            saved_ai.id,
        )
        return VocalEvaluationResponse(id=saved_eval.id)
