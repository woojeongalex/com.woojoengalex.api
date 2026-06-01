import logging

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.orm.ai_vocal_analysis_model import AiVocalAnalysisEntity
from music.adapter.outbound.orm.sing_model import SingEvaluationEntity
from music.adapter.outbound.orm.suggest_model import VocalRecommendationEntity
from music.adapter.outbound.orm.user_vocal_recording_model import UserVocalRecordingEntity
from music.app.ports.output.suggest_repository_port import SuggestRepositoryPort

logger = logging.getLogger(__name__)


class SuggestRepository(SuggestRepositoryPort):
    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    def _require_db(self) -> AsyncSession:
        if self.db is None:
            raise RuntimeError("DB session is not available.")
        return self.db

    async def get_sing_evaluation_by_id(
        self, evaluation_id: int
    ) -> SingEvaluationEntity | None:
        db = self._require_db()
        stmt = select(SingEvaluationEntity).where(SingEvaluationEntity.id == evaluation_id)
        return (await db.execute(stmt)).scalar_one_or_none()

    async def get_ai_analysis_for_sing_evaluation(
        self, sing_evaluation_id: int
    ) -> AiVocalAnalysisEntity | None:
        db = self._require_db()
        stmt = (
            select(AiVocalAnalysisEntity)
            .join(
                UserVocalRecordingEntity,
                AiVocalAnalysisEntity.user_vocal_recording_id
                == UserVocalRecordingEntity.id,
            )
            .where(UserVocalRecordingEntity.sing_evaluation_id == sing_evaluation_id)
        )
        return (await db.execute(stmt)).scalar_one_or_none()

    async def get_ai_analysis_by_id(
        self, ai_analysis_id: int
    ) -> AiVocalAnalysisEntity | None:
        db = self._require_db()
        stmt = select(AiVocalAnalysisEntity).where(
            AiVocalAnalysisEntity.id == ai_analysis_id
        )
        return (await db.execute(stmt)).scalar_one_or_none()

    async def save_recommendation(
        self, row: VocalRecommendationEntity
    ) -> VocalRecommendationEntity:
        db = self._require_db()
        db.add(row)
        await db.commit()
        await db.refresh(row)
        logger.info(
            "[MUSIC][suggest][5/repository] Neon INSERT vocal_recommendations id=%s "
            "for_evaluation=%s ai=%s",
            row.id,
            row.sing_evaluation_id,
            row.ai_vocal_analysis_id,
        )
        return row

    async def get_latest_by_evaluation_id(
        self, sing_evaluation_id: int
    ) -> VocalRecommendationEntity | None:
        db = self._require_db()
        stmt = (
            select(VocalRecommendationEntity)
            .where(
                VocalRecommendationEntity.sing_evaluation_id == sing_evaluation_id,
            )
            .order_by(desc(VocalRecommendationEntity.created_at))
            .limit(1)
        )
        return (await db.execute(stmt)).scalar_one_or_none()
