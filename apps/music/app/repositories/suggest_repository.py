import logging

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from music.app.models.sing_model import VocalSingResultEntity
from music.app.models.suggest_model import VocalRecommendationEntity

logger = logging.getLogger(__name__)


class SuggestRepository:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    def _require_db(self) -> AsyncSession:
        if self.db is None:
            raise RuntimeError("DB session is not available.")
        return self.db

    async def get_sing_result_by_id(
        self, result_id: int
    ) -> VocalSingResultEntity | None:
        db = self._require_db()
        stmt = select(VocalSingResultEntity).where(VocalSingResultEntity.id == result_id)
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
            "for_result=%s",
            row.id,
            row.vocal_sing_result_id,
        )
        return row

    async def get_latest_by_result_id(
        self, vocal_sing_result_id: int
    ) -> VocalRecommendationEntity | None:
        db = self._require_db()
        stmt = (
            select(VocalRecommendationEntity)
            .where(
                VocalRecommendationEntity.vocal_sing_result_id == vocal_sing_result_id,
            )
            .order_by(desc(VocalRecommendationEntity.created_at))
            .limit(1)
        )
        return (await db.execute(stmt)).scalar_one_or_none()
