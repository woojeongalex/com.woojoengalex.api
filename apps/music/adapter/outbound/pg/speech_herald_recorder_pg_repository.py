from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.orm.speech_herald_recorder_model import SpeechRecordingEntity
from music.adapter.outbound.orm.speech_oracle_analyst_model import SpeechEvaluationEntity, SpeechFeedbackAnalysisEntity
from music.adapter.outbound.pg.pg_bundle_repository import save_three_part_bundle
from music.app.dtos.speech_dto import SpeechEvaluationCreateCommand, SpeechEvaluationResultDto
from music.app.ports.output.speech_herald_recorder_repository_port import SpeechRepositoryPort


class HeraldRecorderPgRepository(SpeechRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_evaluation_bundle(
        self, command: SpeechEvaluationCreateCommand
    ) -> SpeechEvaluationResultDto:
        evaluation = SpeechEvaluationEntity(user_id=None)
        recording = SpeechRecordingEntity(
            speech_evaluation_id=0,
            user_id=None,
            topic_id=command.topic_id.strip().lower(),
            file_name=command.file_name or "speech-recording",
            duration_sec=command.duration_sec,
        )
        analysis = SpeechFeedbackAnalysisEntity(
            speech_recording_id=0,
            analysis_engine="client_demo",
            clarity_score=command.clarity_score,
            pace_score=command.pace_score,
            tone_score=command.tone_score,
            summary=command.summary,
            feedback_points=list(command.feedback_points),
        )
        saved_eval, _, _ = await save_three_part_bundle(
            self._session,
            evaluation,
            recording,
            analysis,
            recording_fk_attr="speech_evaluation_id",
            analysis_fk_attr="speech_recording_id",
            log_label="herald",
        )
        return SpeechEvaluationResultDto(id=saved_eval.id)
