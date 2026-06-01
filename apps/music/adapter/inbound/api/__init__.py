from fastapi import APIRouter

from music.adapter.inbound.api.v1.evaluation_router import evaluation_router
from music.adapter.inbound.api.v1.instrument_router import instrument_router
from music.adapter.inbound.api.v1.search_router import search_router
from music.adapter.inbound.api.v1.speech_router import speech_router
from music.adapter.inbound.api.v1.suggest_router import suggest_router
from music.adapter.inbound.api.v1.video_router import video_router

music_router = APIRouter()

music_router.include_router(search_router)
music_router.include_router(evaluation_router)
music_router.include_router(suggest_router)
music_router.include_router(instrument_router)
music_router.include_router(speech_router)
music_router.include_router(video_router)

__all__ = ["music_router"]
