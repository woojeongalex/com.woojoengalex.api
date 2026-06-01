import logging

from music.adapter.outbound.orm.ai_vocal_analysis_model import AiVocalAnalysisEntity
from music.adapter.outbound.orm.evaluation_models import SingEvaluationEntity
from music.adapter.outbound.orm.user_vocal_recording_model import UserVocalRecordingEntity
from music.app.dtos.evaluation_dto import (
    VocalEvaluationCreateCommand,
    VocalEvaluationResultDto,
)
from music.app.ports.input.evaluation_use_case import EvaluationUseCase
from music.app.ports.output.evaluation_repository_port import EvaluationRepositoryPort
from music.app.ports.output.list_repository_port import ListRepositoryPort

logger = logging.getLogger(__name__)


class EvaluationService(EvaluationUseCase):
    """평가 요청을 세션(허브) → 녹음 → AI 분석으로 분리 저장 (3NF)."""

    def __init__(
        self,
        repository: EvaluationRepositoryPort,
        list_repository: ListRepositoryPort,
    ) -> None:
        self._repository = repository
        self._list_repository = list_repository

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
        self, command: VocalEvaluationCreateCommand
    ) -> VocalEvaluationResultDto:
        catalog_song_id, mr_search_list_id = await self._resolve_catalog_and_mr(
            command.catalog_song_id,
            command.mr_search_list_id,
        )

        engine = "librosa" if command.input_source == "video" else "mic_demo"

        file_name = command.file_name or ""
        user_id: int | None = None

        evaluation = SingEvaluationEntity(user_id=user_id)
        vocal_recording = UserVocalRecordingEntity(
            sing_evaluation_id=0,
            user_id=user_id,
            catalog_song_id=catalog_song_id,
            mr_search_list_id=mr_search_list_id,
            input_source=command.input_source,
            file_name=file_name,
            duration_sec=command.duration_sec,
        )
        ai_analysis = AiVocalAnalysisEntity(
            user_vocal_recording_id=0,
            analysis_engine=engine,
            pitch_score=command.pitch_score,
            rhythm_score=command.rhythm_score,
            vocal_grade=command.vocal_grade,
            summary=command.summary,
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
        return VocalEvaluationResultDto(id=saved_eval.id)
