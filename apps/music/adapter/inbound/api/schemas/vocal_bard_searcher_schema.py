from pydantic import BaseModel, ConfigDict, Field


class SongMrHitResponse(BaseModel):
    id: int
    catalog_song_id: str = Field(alias="catalogSongId")
    title: str
    artist: str
    bpm: int
    song_key: str = Field(alias="songKey")
    range_label: str = Field(alias="rangeLabel")
    mr_track_name: str = Field(alias="mrTrackName")
    mr_description: str = Field(alias="mrDescription")

    model_config = ConfigDict(populate_by_name=True)


class SongMrSearchResponse(BaseModel):
    query: str
    hits: list[SongMrHitResponse]
    count: int
