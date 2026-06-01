import logging

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.inbound.api.mappers.music_inbound_mapper import to_search_response
from music.adapter.inbound.api.schemas.list_schema import SongMrSearchResponse
from music.adapter.outbound.pg.list_pg_repository import ListRepository
from music.app.ports.input.search_use_case import SearchUseCase
from music.app.use_cases.list_service import ListService

logger = logging.getLogger(__name__)
search_router = APIRouter(tags=["music-search"])


def _use_case(db: AsyncSession) -> SearchUseCase:
    return ListService(ListRepository(db))


@search_router.get("/api/songs/search", response_model=SongMrSearchResponse)
async def songs_search(
    q: str = Query(..., min_length=1, description="노래 제목·MR·아티스트 검색어"),
    db: AsyncSession = Depends(get_db),
) -> SongMrSearchResponse:
    logger.info("[MUSIC][search][1/router] GET /api/songs/search q=%s", q.strip())
    try:
        dto = await _use_case(db).search_and_persist(q)
        logger.info(
            "[MUSIC][search][1/router] 완료 q=%s count=%s titles=%s",
            dto.query,
            dto.count,
            [h.title for h in dto.hits],
        )
        return to_search_response(dto)
    except SQLAlchemyError as exc:
        logger.exception("[music] GET /api/songs/search DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
