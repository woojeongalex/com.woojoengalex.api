from fastapi import APIRouter, Depends, Query

from music.adapter.inbound.api.deps.music_deps import get_instrument_use_case
from music.adapter.inbound.api.handlers.instrument_inbound_handlers import pass_instrument_evaluation
from music.adapter.inbound.api.mappers.music_inbound_mapper import (
    from_instrument_create,
    to_instrument_catalog_response,
    to_instrument_response,
)
from music.adapter.inbound.api.schemas.instrument_schemas import (
    InstrumentCatalogResponse,
    InstrumentEvaluationCreateRequest,
    InstrumentEvaluationResponse,
)
from music.app.ports.input.instrument_use_case import InstrumentUseCase

instrument_router = APIRouter(tags=["music-instrument"])


@instrument_router.get("/api/music/instrument-catalog", response_model=InstrumentCatalogResponse)
async def get_instrument_catalog(
    q: str = Query("", description="악기 검색어"),
    instrument: InstrumentUseCase = Depends(get_instrument_use_case),
) -> InstrumentCatalogResponse:
    return to_instrument_catalog_response(instrument.search(q))


@instrument_router.post(
    "/api/music/instrument-evaluation",
    response_model=InstrumentEvaluationResponse,
)
async def post_instrument_evaluation(
    body: InstrumentEvaluationCreateRequest,
    instrument: InstrumentUseCase = Depends(get_instrument_use_case),
) -> InstrumentEvaluationResponse:
    result = await pass_instrument_evaluation(instrument, from_instrument_create(body))
    return to_instrument_response(result)
