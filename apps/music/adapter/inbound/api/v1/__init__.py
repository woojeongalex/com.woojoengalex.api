from music.adapter.inbound.api.v1.evaluation_router import evaluation_router
from music.adapter.inbound.api.v1.instrument_router import instrument_router
from music.adapter.inbound.api.v1.search_router import search_router
from music.adapter.inbound.api.v1.speech_router import speech_router
from music.adapter.inbound.api.v1.suggest_router import suggest_router
from music.adapter.inbound.api.v1.video_router import video_router

__all__ = [
    "search_router",
    "evaluation_router",
    "suggest_router",
    "instrument_router",
    "speech_router",
    "video_router",
]
