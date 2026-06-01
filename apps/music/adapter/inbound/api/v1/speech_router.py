import logging

from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

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
from music.adapter.outbound.pg.speech_pg_repository import SpeechRepository
from music.app.ports.input.speech_use_case import SpeechUseCase
from music.app.use_cases.speech_service import SpeechService

logger = logging.getLogger(__name__)
speech_router = APIRouter(tags=["music-speech"])


def _interactor(db: AsyncSession | None) -> SpeechUseCase:
    return SpeechService(SpeechRepository(db))


@speech_router.get("/api/music/speech-topics", response_model=SpeechTopicsResponse)
async def get_speech_topics() -> SpeechTopicsResponse:
    return to_speech_topics_response(_interactor(None).list_topics())


@speech_router.post("/api/music/speech-evaluation", response_model=SpeechEvaluationResponse)
async def post_speech_evaluation(
    body: SpeechEvaluationCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> SpeechEvaluationResponse:
    try:
        result = await _interactor(db).save_evaluation(from_speech_create(body))
        return to_speech_response(result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][speech] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
