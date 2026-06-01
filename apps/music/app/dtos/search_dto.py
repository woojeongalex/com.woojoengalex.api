from dataclasses import dataclass


@dataclass(frozen=True)
class SongMrHitDto:
    id: int
    catalog_song_id: str
    title: str
    artist: str
    bpm: int
    song_key: str
    range_label: str
    mr_track_name: str
    mr_description: str


@dataclass(frozen=True)
class SongMrSearchResultDto:
    query: str
    hits: list[SongMrHitDto]
    count: int
