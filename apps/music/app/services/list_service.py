import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.catalog import find_vocal_catalog_by_query
from music.app.models.list_model import SongMrSearchListEntity
from music.app.repositories.list_repository import ListRepository
from music.app.schemas.list_schema import SongMrHitResponse, SongMrSearchResponse

logger = logging.getLogger(__name__)


class ListService:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self._repository = ListRepository(db)

    async def search_and_persist(self, raw_query: str) -> SongMrSearchResponse:
        q = raw_query.strip()
        matches = find_vocal_catalog_by_query(q)
        entities = [
            SongMrSearchListEntity(
                search_query=q,
                catalog_song_id=item.id,
                title=item.title,
                artist=item.artist,
                bpm=item.bpm,
                song_key=item.key,
                range_label=item.range_label,
                mr_track_name=item.mr_track_name,
                mr_description=item.mr_description,
            )
            for item in matches
        ]
        if not entities:
            logger.info(
                "[MUSIC][search][4/service] MR search query=%s match_count=0 (DB 저장 없음)",
                q,
            )
            return SongMrSearchResponse(query=q, hits=[], count=0)
        saved = await self._repository.save_search_results(entities)
        logger.info(
            "[MUSIC][search][4/service] MR search query=%s persisted_rows=%s titles=%s",
            q,
            len(saved),
            [e.title for e in saved],
        )
        hits = [
            SongMrHitResponse(
                id=e.id,
                catalog_song_id=e.catalog_song_id,
                title=e.title,
                artist=e.artist,
                bpm=e.bpm,
                song_key=e.song_key,
                range_label=e.range_label,
                mr_track_name=e.mr_track_name,
                mr_description=e.mr_description,
            )
            for e in saved
        ]
        return SongMrSearchResponse(query=q, hits=hits, count=len(hits))
