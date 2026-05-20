import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.models.result_models import AiVocalAnalysisResultEntity

logger = logging.getLogger(__name__)


class ResultRepository:
    """AI 분석 결과 → Neon `vocal_sing_results` INSERT."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    def _require_db(self) -> AsyncSession:
        if self.db is None:
            raise RuntimeError("DB session is not available.")
        return self.db

    async def save_ai_analysis_result(
        self, row: AiVocalAnalysisResultEntity
    ) -> AiVocalAnalysisResultEntity:
        db = self._require_db()
        db.add(row)
        await db.commit()
        await db.refresh(row)
        logger.info(
            "[MUSIC][result][5/repository] Neon INSERT vocal_sing_results id=%s input=%s",
            row.id,
            row.input_source,
        )
        return row
