from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.orm.speech_evaluation_model import SpeechEvaluationEntity
from music.adapter.outbound.orm.speech_feedback_analysis_model import (
    SpeechFeedbackAnalysisEntity,
)
from music.adapter.outbound.orm.speech_recording_model import SpeechRecordingEntity
from music.adapter.outbound.pg.pg_bundle_repository import save_three_part_bundle
from music.app.ports.output.speech_repository_port import SpeechRepositoryPort


class SpeechRepository(SpeechRepositoryPort):
    def __init__(self, db: AsyncSession | None = None) -> None:
        self._db = db

    def _require_db(self) -> AsyncSession:
        if self._db is None:
            raise RuntimeError("DB session is not available.")
        return self._db

    async def save_evaluation_bundle(
        self,
        evaluation: SpeechEvaluationEntity,
        recording: SpeechRecordingEntity,
        analysis: SpeechFeedbackAnalysisEntity,
    ) -> tuple[SpeechEvaluationEntity, SpeechRecordingEntity, SpeechFeedbackAnalysisEntity]:
        return await save_three_part_bundle(
            self._require_db(),
            evaluation,
            recording,
            analysis,
            recording_fk_attr="speech_evaluation_id",
            analysis_fk_attr="speech_recording_id",
            log_label="speech",
        )
