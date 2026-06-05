from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.orm.speech_evaluation_model import SpeechEvaluationEntity
from music.adapter.outbound.orm.speech_feedback_analysis_model import (
    SpeechFeedbackAnalysisEntity,
)
from music.adapter.outbound.orm.speech_recording_model import SpeechRecordingEntity
from music.adapter.outbound.pg.pg_bundle_repository import save_three_part_bundle
from music.app.ports.output.speech_repository_port import SpeechRepositoryPort


class SpeechPgRepository(SpeechRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_evaluation_bundle(
        self,
        evaluation: SpeechEvaluationEntity,
        recording: SpeechRecordingEntity,
        analysis: SpeechFeedbackAnalysisEntity,
    ) -> tuple[SpeechEvaluationEntity, SpeechRecordingEntity, SpeechFeedbackAnalysisEntity]:
        return await save_three_part_bundle(
            self._session,
            evaluation,
            recording,
            analysis,
            recording_fk_attr="speech_evaluation_id",
            analysis_fk_attr="speech_recording_id",
            log_label="speech",
        )
