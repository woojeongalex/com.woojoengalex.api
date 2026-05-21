import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.models.evaluation_models import AiVocalAnalysisEvaluationEntity

logger = logging.getLogger(__name__)


class EvaluationRepository:
    """보컬 평가 → Neon `sing_evaluations` INSERT."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    def _require_db(self) -> AsyncSession:
        if self.db is None:
            raise RuntimeError("DB session is not available.")
        return self.db

    async def save_evaluation(
        self, row: AiVocalAnalysisEvaluationEntity
    ) -> AiVocalAnalysisEvaluationEntity:
        db = self._require_db()
        db.add(row)
        await db.commit()
        await db.refresh(row)
        logger.info(
            "[MUSIC][evaluation][5/repository] Neon INSERT sing_evaluations id=%s input=%s",
            row.id,
            row.input_source,
        )
        return row
