import logging

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from music.app.models.sing_model import SingEvaluationEntity
from music.app.models.suggest_model import VocalRecommendationEntity

logger = logging.getLogger(__name__)


class SuggestRepository:
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

    async def save_recommendation(
        self, row: VocalRecommendationEntity
    ) -> VocalRecommendationEntity:
        db = self._require_db()
        db.add(row)
        await db.commit()
        await db.refresh(row)
        logger.info(
            "[MUSIC][suggest][5/repository] Neon INSERT vocal_recommendations id=%s "
            "for_evaluation=%s",
            row.id,
            row.sing_evaluation_id,
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
