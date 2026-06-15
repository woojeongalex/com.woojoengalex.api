"""[Layer: Ports] MR 검색 목록 출력 Port — Neon/Postgres 저장 계약."""
from __future__ import annotations

from abc import ABC, abstractmethod

from music.app.dtos.search_dto import SongMrHitDto, SongMrSearchSaveDto


class ListRepositoryPort(ABC):
    @abstractmethod
    async def get_by_id(self, mr_id: int) -> SongMrHitDto | None:
        pass

    @abstractmethod
    async def save_search_results(
        self, items: list[SongMrSearchSaveDto]
    ) -> list[SongMrHitDto]:
        pass
