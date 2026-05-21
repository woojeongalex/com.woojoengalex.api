import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.models.sing_model import SingEvaluationEntity

logger = logging.getLogger(__name__)


class SingRepository:
    """보컬 평가 → Neon `sing_evaluations` INSERT."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    def _require_db(self) -> AsyncSession:
        if self.db is None:
            raise RuntimeError("DB session is not available.")
        return self.db

    async def save_sing_evaluation(
        self, row: SingEvaluationEntity
    ) -> SingEvaluationEntity:
        db = self._require_db()
        db.add(row)
        await db.commit()
        await db.refresh(row)
        logger.info(
            "[MUSIC][sing][5/repository] Neon INSERT sing_evaluations id=%s input=%s",
            row.id,
            row.input_source,
        )
        return row
