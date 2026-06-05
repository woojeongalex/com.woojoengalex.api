from fastapi import APIRouter, Depends

from music.adapter.inbound.api.deps.music_deps import get_speech_use_case
from music.adapter.inbound.api.handlers.speech_inbound_handlers import pass_speech_evaluation
from music.adapter.inbound.api.mappers.music_inbound_mapper import (
    from_speech_create,
    to_speech_response,
    to_speech_topics_response,
)
from music.adapter.inbound.api.schemas.speech_schemas import (
    SpeechEvaluationCreateRequest,
    SpeechEvaluationResponse,
    SpeechTopicsResponse,
)
from music.app.ports.input.speech_use_case import SpeechUseCase

speech_router = APIRouter(tags=["music-speech"])


@speech_router.get("/api/music/speech-topics", response_model=SpeechTopicsResponse)
async def get_speech_topics(
    speech: SpeechUseCase = Depends(get_speech_use_case),
) -> SpeechTopicsResponse:
    return to_speech_topics_response(speech.read_topics())


@speech_router.post("/api/music/speech-evaluation", response_model=SpeechEvaluationResponse)
async def post_speech_evaluation(
    body: SpeechEvaluationCreateRequest,
    speech: SpeechUseCase = Depends(get_speech_use_case),
) -> SpeechEvaluationResponse:
    result = await pass_speech_evaluation(speech, from_speech_create(body))
    return to_speech_response(result)
