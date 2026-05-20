import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.schemas.list_schema import SongMrSearchResponse
from music.app.services.list_service import ListService
logger = logging.getLogger(__name__)


class ListController:
    """MR/노래 검색 — Service에 위임."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._service = ListService(db)

    async def search_mr(self, query: str) -> SongMrSearchResponse:
        logger.info(
            "[MUSIC][search][2/controller] → service.search_and_persist q=%s",
            query.strip(),
        )
        return await self._service.search_and_persist(query)
