import logging

from music.adapter.outbound.orm.speech_evaluation_model import SpeechEvaluationEntity
from music.adapter.outbound.orm.speech_feedback_analysis_model import (
    SpeechFeedbackAnalysisEntity,
)
from music.adapter.outbound.orm.speech_recording_model import SpeechRecordingEntity
from music.app.dtos.speech_dto import (
    SpeechEvaluationCreateCommand,
    SpeechEvaluationResultDto,
    SpeechTopicHitDto,
    SpeechTopicsResultDto,
)
from music.app.ports.input.speech_use_case import SpeechUseCase
from music.app.ports.output.speech_repository_port import SpeechRepositoryPort
from music.app.speech_catalog import get_speech_topic, list_speech_topics

logger = logging.getLogger(__name__)


class SpeechService(SpeechUseCase):
    def __init__(self, repository: SpeechRepositoryPort) -> None:
        self._repository = repository

    def list_topics(self) -> SpeechTopicsResultDto:
        hits = [
            SpeechTopicHitDto(
                topic_id=item.topic_id,
                label=item.label,
                description=item.description,
            )
            for item in list_speech_topics()
        ]
        return SpeechTopicsResultDto(hits=hits, count=len(hits))

    async def save_evaluation(
        self, command: SpeechEvaluationCreateCommand
    ) -> SpeechEvaluationResultDto:
        if get_speech_topic(command.topic_id) is None:
            raise ValueError("지원하지 않는 스피치 주제입니다.")

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
            feedback_points=command.feedback_points,
        )
        saved_eval, _, _ = await self._repository.save_evaluation_bundle(
            evaluation,
            recording,
            analysis,
        )
        logger.info("[MUSIC][speech][service] 저장 eval=%s", saved_eval.id)
        return SpeechEvaluationResultDto(id=saved_eval.id)
