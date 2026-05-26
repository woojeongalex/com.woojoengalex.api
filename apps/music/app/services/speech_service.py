import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.models.speech_evaluation_model import SpeechEvaluationEntity
from music.app.models.speech_feedback_analysis_model import SpeechFeedbackAnalysisEntity
from music.app.models.speech_recording_model import SpeechRecordingEntity
from music.app.repositories.bundle_repository import save_three_part_bundle
from music.app.schemas.speech_schemas import (
    SpeechEvaluationCreateRequest,
    SpeechEvaluationResponse,
    SpeechTopicHit,
    SpeechTopicsResponse,
)
from music.app.speech_catalog import get_speech_topic, list_speech_topics

logger = logging.getLogger(__name__)


class SpeechService:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self._db = db

    def _require_db(self) -> AsyncSession:
        if self._db is None:
            raise RuntimeError("DB session is not available.")
        return self._db

    def list_topics(self) -> SpeechTopicsResponse:
        hits = [
            SpeechTopicHit(
                topic_id=item.topic_id,
                label=item.label,
                description=item.description,
            )
            for item in list_speech_topics()
        ]
        return SpeechTopicsResponse(hits=hits, count=len(hits))

    async def save_evaluation(
        self, body: SpeechEvaluationCreateRequest
    ) -> SpeechEvaluationResponse:
        if get_speech_topic(body.topic_id) is None:
            raise ValueError("지원하지 않는 스피치 주제입니다.")

        evaluation = SpeechEvaluationEntity(user_id=None)
        recording = SpeechRecordingEntity(
            speech_evaluation_id=0,
            user_id=None,
            topic_id=body.topic_id.strip().lower(),
            file_name=body.file_name or "speech-recording",
            duration_sec=body.duration_sec,
        )
        analysis = SpeechFeedbackAnalysisEntity(
            speech_recording_id=0,
            analysis_engine="client_demo",
            clarity_score=body.clarity_score,
            pace_score=body.pace_score,
            tone_score=body.tone_score,
            summary=body.summary,
            feedback_points=body.feedback_points,
        )
        saved_eval, _, _ = await save_three_part_bundle(
            self._require_db(),
            evaluation,
            recording,
            analysis,
            recording_fk_attr="speech_evaluation_id",
            analysis_fk_attr="speech_recording_id",
            log_label="speech",
        )
        logger.info("[MUSIC][speech][service] 저장 eval=%s", saved_eval.id)
        return SpeechEvaluationResponse(id=saved_eval.id)
