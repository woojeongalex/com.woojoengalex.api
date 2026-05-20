import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.models.list_model import SongMrSearchListEntity
logger = logging.getLogger(__name__)


class ListRepository:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    def _require_db(self) -> AsyncSession:
        if self.db is None:
            raise RuntimeError("DB session is not available.")
        return self.db

    async def save_search_results(
        self, rows: list[SongMrSearchListEntity]
    ) -> list[SongMrSearchListEntity]:
        """매칭된 곡마다 한 행씩 저장하고 PK를 채운 뒤 반환."""
        db = self._require_db()
        if not rows:
            return []
        db.add_all(rows)
        await db.commit()
        for row in rows:
            await db.refresh(row)
        logger.info(
            "[MUSIC][search][5/repository] Neon commit song_mr_search_lists rows=%s ids=%s",
            len(rows),
            [r.id for r in rows],
        )
        return rows
