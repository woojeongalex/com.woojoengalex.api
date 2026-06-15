from fastapi import APIRouter, Depends

from music.adapter.inbound.api.mappers.music_inbound_mapper import from_speech_create, to_speech_response
from music.adapter.inbound.api.schemas.speech_herald_recorder_schema import SpeechEvaluationCreateRequest
from music.adapter.inbound.api.schemas.speech_oracle_analyst_schema import SpeechEvaluationResponse
from music.app.ports.input.speech_herald_recorder_use_case import SpeechEvaluationUseCase
from music.adapter.inbound.api.deps.music_deps import get_speech_recorder_use_case

speech_herald_recorder_router = APIRouter(tags=["music-speech"])


@speech_herald_recorder_router.post("/api/music/speech-evaluation", response_model=SpeechEvaluationResponse)
async def post_speech_evaluation(
    body: SpeechEvaluationCreateRequest,
    speech: SpeechEvaluationUseCase = Depends(get_speech_recorder_use_case),
) -> SpeechEvaluationResponse:
    return to_speech_response(await speech.upload(from_speech_create(body)))
