import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from music.app.dtos.search_dto import SongMrSearchResultDto
from music.app.ports.input.search_use_case import SearchUseCase

logger = logging.getLogger(__name__)


async def pass_songs_search(
    search: SearchUseCase,
    raw_query: str,
) -> SongMrSearchResultDto:
    try:
        return await search.search(raw_query)
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][search][handler] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
