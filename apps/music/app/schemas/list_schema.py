from pydantic import BaseModel, Field


class SongMrHitResponse(BaseModel):
    """DB에 저장된 검색 결과 1건."""

    id: int = Field(description="시스템 PK (song_mr_search_lists.id)")
    catalog_song_id: str
    title: str
    artist: str
    bpm: int
    song_key: str
    range_label: str
    mr_track_name: str
    mr_description: str


class SongMrSearchResponse(BaseModel):
    query: str
    hits: list[SongMrHitResponse]
    count: int
