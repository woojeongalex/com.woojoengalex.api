"""[Layer: Ports] 악기 카탈로그 입력 Port — 카탈로그 검색 (inbound → usecase)."""
from __future__ import annotations

from abc import ABC, abstractmethod

from music.app.dtos.instrument_dto import InstrumentCatalogResultDto


class InstrumentCatalogUseCase(ABC):
    @abstractmethod
    def search(self, q: str = "") -> InstrumentCatalogResultDto:
        pass
