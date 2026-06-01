import logging

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.inbound.api.mappers.music_inbound_mapper import (
    from_suggest_create,
    to_suggest_response,
)
from music.adapter.inbound.api.schemas.suggest_schema import (
    VocalRecommendationCreateRequest,
    VocalRecommendationResponse,
)
from music.adapter.outbound.pg.suggest_pg_repository import SuggestRepository
from music.app.ports.input.suggest_use_case import SuggestUseCase
from music.app.use_cases.suggest_service import SuggestService

logger = logging.getLogger(__name__)
suggest_router = APIRouter(tags=["music-suggest"])


def _use_case(db: AsyncSession) -> SuggestUseCase:
    return SuggestService(SuggestRepository(db))


@suggest_router.post("/api/music/vocal-recommendations", response_model=VocalRecommendationResponse)
async def post_vocal_recommendations(
    body: VocalRecommendationCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> VocalRecommendationResponse:
    logger.info(
        "[MUSIC][suggest][1/router] POST /api/music/vocal-recommendations singEvaluationId=%s",
        body.sing_evaluation_id,
    )
    try:
        result = await _use_case(db).create_from_saved_evaluation(from_suggest_create(body))
        return to_suggest_response(result)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][suggest][1/router] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc


@suggest_router.get("/api/music/vocal-recommendations", response_model=VocalRecommendationResponse)
async def get_vocal_recommendations(
    singEvaluationId: int = Query(
        ...,
        ge=1,
        alias="singEvaluationId",
        description="sing_evaluations.id",
    ),
    db: AsyncSession = Depends(get_db),
) -> VocalRecommendationResponse:
    logger.info(
        "[MUSIC][suggest][1/router] GET /api/music/vocal-recommendations singEvaluationId=%s",
        singEvaluationId,
    )
    try:
        dto = await _use_case(db).get_latest(singEvaluationId)
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][suggest][1/router] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
    if dto is None:
        raise HTTPException(
            status_code=404,
            detail="해당 분석에 대한 추천이 없습니다. 먼저 POST로 생성하세요.",
        )
    return to_suggest_response(dto)
