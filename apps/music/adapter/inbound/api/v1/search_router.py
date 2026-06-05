from fastapi import APIRouter, Depends, Query

from music.adapter.inbound.api.deps.music_deps import get_search_use_case
from music.adapter.inbound.api.handlers.search_inbound_handlers import pass_songs_search
from music.adapter.inbound.api.mappers.music_inbound_mapper import to_search_response
from music.adapter.inbound.api.schemas.list_schema import SongMrSearchResponse
from music.app.ports.input.search_use_case import SearchUseCase

search_router = APIRouter(tags=["music-search"])


@search_router.get("/api/songs/search", response_model=SongMrSearchResponse)
async def songs_search(
    q: str = Query(..., min_length=1, description="노래 제목·MR·아티스트 검색어"),
    search: SearchUseCase = Depends(get_search_use_case),
) -> SongMrSearchResponse:
    dto = await pass_songs_search(search, q)
    return to_search_response(dto)
