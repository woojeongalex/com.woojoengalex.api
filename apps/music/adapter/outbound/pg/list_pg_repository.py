import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.orm.list_model import SongMrSearchListEntity
from music.app.ports.output.list_repository_port import ListRepositoryPort
logger = logging.getLogger(__name__)


class ListPgRepository(ListRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, mr_id: int) -> SongMrSearchListEntity | None:
        db = self._session
        stmt = select(SongMrSearchListEntity).where(SongMrSearchListEntity.id == mr_id)
        return (await db.execute(stmt)).scalar_one_or_none()

    async def save_search_results(
        self, rows: list[SongMrSearchListEntity]
    ) -> list[SongMrSearchListEntity]:
        """매칭된 곡마다 한 행씩 저장하고 PK를 채운 뒤 반환."""
        db = self._session
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
