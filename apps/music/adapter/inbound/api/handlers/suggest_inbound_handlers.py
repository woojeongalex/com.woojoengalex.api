import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from music.app.dtos.suggest_dto import (
    VocalRecommendationCreateCommand,
    VocalRecommendationResultDto,
)
from music.app.ports.input.suggest_use_case import SuggestUseCase

logger = logging.getLogger(__name__)


async def pass_vocal_recommendation_upload(
    suggest: SuggestUseCase,
    command: VocalRecommendationCreateCommand,
) -> VocalRecommendationResultDto:
    try:
        return await suggest.upload(command)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][suggest][handler] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc


async def pass_vocal_recommendation_read(
    suggest: SuggestUseCase,
    sing_evaluation_id: int,
) -> VocalRecommendationResultDto:
    try:
        dto = await suggest.read(sing_evaluation_id)
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][suggest][handler] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
    if dto is None:
        raise HTTPException(
            status_code=404,
            detail="해당 분석에 대한 추천이 없습니다. 먼저 POST로 생성하세요.",
        )
    return dto
