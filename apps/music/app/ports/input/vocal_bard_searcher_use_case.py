"""[Layer: Ports] MR 검색 입력 Port — 검색·저장 (inbound → usecase)."""
from __future__ import annotations

from abc import ABC, abstractmethod

from music.app.dtos.search_dto import SongMrSearchResultDto


class SearchUseCase(ABC):
    @abstractmethod
    async def search(self, raw_query: str) -> SongMrSearchResultDto:
        pass
