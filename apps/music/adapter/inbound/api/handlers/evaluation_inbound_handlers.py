import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from music.app.dtos.evaluation_dto import (
    VocalEvaluationCreateCommand,
    VocalEvaluationResultDto,
)
from music.app.ports.input.evaluation_use_case import EvaluationUseCase

logger = logging.getLogger(__name__)


async def pass_sing_evaluation(
    evaluation: EvaluationUseCase,
    command: VocalEvaluationCreateCommand,
) -> VocalEvaluationResultDto:
    try:
        return await evaluation.upload(command)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][sing][handler] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
