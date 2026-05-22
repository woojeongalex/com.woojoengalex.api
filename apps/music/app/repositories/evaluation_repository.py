import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.models.ai_vocal_analysis_model import AiVocalAnalysisEntity
from music.app.models.evaluation_models import SingEvaluationEntity
from music.app.models.user_vocal_recording_model import UserVocalRecordingEntity

logger = logging.getLogger(__name__)


class EvaluationRepository:
    """세션 + 녹음 + AI(녹음 대상) → Neon INSERT (한 트랜잭션)."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    def _require_db(self) -> AsyncSession:
        if self.db is None:
            raise RuntimeError("DB session is not available.")
        return self.db

    async def save_evaluation_bundle(
        self,
        evaluation: SingEvaluationEntity,
        vocal_recording: UserVocalRecordingEntity,
        ai_analysis: AiVocalAnalysisEntity,
    ) -> tuple[SingEvaluationEntity, UserVocalRecordingEntity, AiVocalAnalysisEntity]:
        db = self._require_db()
        db.add(evaluation)
        await db.flush()
        eval_id = evaluation.id
        assert eval_id is not None

        vocal_recording.sing_evaluation_id = eval_id
        db.add(vocal_recording)
        await db.flush()
        recording_id = vocal_recording.id
        assert recording_id is not None

        ai_analysis.user_vocal_recording_id = recording_id
        db.add(ai_analysis)
        await db.commit()
        await db.refresh(evaluation)
        await db.refresh(vocal_recording)
        await db.refresh(ai_analysis)
        logger.info(
            "[MUSIC][evaluation][5/repository] Neon INSERT eval=%s recording=%s "
            "ai=%s (ai→recording)",
            evaluation.id,
            vocal_recording.id,
            ai_analysis.id,
        )
        return evaluation, vocal_recording, ai_analysis
