from fastapi import APIRouter, Depends

from music.adapter.inbound.api.mappers.music_inbound_mapper import to_speech_topics_response
from music.adapter.inbound.api.schemas.speech_cicero_topic_schema import SpeechTopicsResponse
from music.app.ports.input.speech_cicero_topic_use_case import SpeechTopicUseCase
from music.adapter.inbound.api.deps.music_deps import get_speech_topic_use_case

speech_cicero_topic_router = APIRouter(tags=["music-speech"])


@speech_cicero_topic_router.get("/api/music/speech-topics", response_model=SpeechTopicsResponse)
async def get_speech_topics(
    speech: SpeechTopicUseCase = Depends(get_speech_topic_use_case),
) -> SpeechTopicsResponse:
    return to_speech_topics_response(speech.read_topics())
