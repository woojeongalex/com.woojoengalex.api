from fastapi import APIRouter, Depends

from music.adapter.inbound.api.mappers.music_inbound_mapper import from_instrument_create, to_instrument_response
from music.adapter.inbound.api.schemas.instrument_andrew_recorder_schema import InstrumentEvaluationCreateRequest
from music.adapter.inbound.api.schemas.instrument_fletcher_tuner_schema import InstrumentEvaluationResponse
from music.app.ports.input.instrument_andrew_recorder_use_case import InstrumentEvaluationUseCase
from music.adapter.inbound.api.deps.music_deps import get_instrument_recorder_use_case

instrument_andrew_recorder_router = APIRouter(tags=["music-instrument"])


@instrument_andrew_recorder_router.post(
    "/api/music/instrument-evaluation",
    response_model=InstrumentEvaluationResponse,
)
async def post_instrument_evaluation(
    body: InstrumentEvaluationCreateRequest,
    instrument: InstrumentEvaluationUseCase = Depends(get_instrument_recorder_use_case),
) -> InstrumentEvaluationResponse:
    return to_instrument_response(await instrument.upload(from_instrument_create(body)))
