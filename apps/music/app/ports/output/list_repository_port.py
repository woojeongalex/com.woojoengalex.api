"""[Layer: Ports] MR 검색 목록 출력 Port — Neon/Postgres 저장 계약."""

from abc import ABC, abstractmethod

from music.adapter.outbound.orm.list_model import SongMrSearchListEntity


class ListRepositoryPort(ABC):
    @abstractmethod
    async def get_by_id(self, mr_id: int) -> SongMrSearchListEntity | None:
        pass

    @abstractmethod
    async def save_search_results(
        self, rows: list[SongMrSearchListEntity]
    ) -> list[SongMrSearchListEntity]:
        pass
