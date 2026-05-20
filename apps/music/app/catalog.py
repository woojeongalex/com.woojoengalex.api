"""MR/보컬 곡 목록 (데모). 프론트 `vocal-song-catalog` 와 동일 기준으로 유지."""

from dataclasses import dataclass


@dataclass(frozen=True)
class VocalCatalogItem:
    id: str
    title: str
    artist: str
    bpm: int
    key: str
    range_label: str
    mr_track_name: str
    mr_description: str


VOCAL_CATALOG: tuple[VocalCatalogItem, ...] = (
    VocalCatalogItem(
        id="spring-day",
        title="봄날",
        artist="BTS",
        bpm=106,
        key="E Major",
        range_label="중저음 중심",
        mr_track_name="봄날 (Official MR · Inst.)",
        mr_description="원곡 키·템포 기준 반주 트랙",
    ),
    VocalCatalogItem(
        id="through-the-night",
        title="밤편지",
        artist="IU",
        bpm=79,
        key="C Major",
        range_label="감성 발라드",
        mr_track_name="밤편지 (MR · 피아노 반주)",
        mr_description="피아노 위주 반주, 보컬 가이드 없음",
    ),
    VocalCatalogItem(
        id="defying-gravity",
        title="Defying Gravity",
        artist="Wicked",
        bpm=84,
        key="F Major",
        range_label="벨팅과 호흡 컨트롤 중심",
        mr_track_name="Defying Gravity (Show MR)",
        mr_description="뮤지컬 쇼버전 길이·구성 기준 반주",
    ),
)


def find_vocal_catalog_by_query(query: str) -> list[VocalCatalogItem]:
    q = query.strip().lower()
    if not q:
        return []
    out: list[VocalCatalogItem] = []
    for item in VOCAL_CATALOG:
        if (
            q in item.title.lower()
            or q in item.mr_track_name.lower()
            or q in item.artist.lower()
        ):
            out.append(item)
    return out
