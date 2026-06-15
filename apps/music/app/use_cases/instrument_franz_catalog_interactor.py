from __future__ import annotations

import logging

from music.app.dtos.instrument_dto import InstrumentCatalogHitDto, InstrumentCatalogResultDto
from music.app.ports.input.instrument_franz_catalog_use_case import InstrumentCatalogUseCase
from music.domain.instrument_franz_catalog import search_instruments

logger = logging.getLogger(__name__)


class FranzCatalogInteractor(InstrumentCatalogUseCase):
    def search(self, q: str = "") -> InstrumentCatalogResultDto:
        hits = [
            InstrumentCatalogHitDto(
                instrument_id=item.instrument_id,
                label=item.label,
                description=item.description,
                standard_tuning=item.standard_tuning,
            )
            for item in search_instruments(q)
        ]
        logger.info("[MUSIC][franz][4/interactor] 카탈로그 검색 q=%r hits=%d", q, len(hits))
        return InstrumentCatalogResultDto(query=q.strip(), hits=hits, count=len(hits))
