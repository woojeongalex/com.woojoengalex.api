import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from music.app.dtos.instrument_dto import InstrumentEvaluationCreateCommand, InstrumentEvaluationResultDto
from music.app.ports.input.instrument_use_case import InstrumentUseCase

logger = logging.getLogger(__name__)


async def pass_instrument_evaluation(
    instrument: InstrumentUseCase,
    command: InstrumentEvaluationCreateCommand,
) -> InstrumentEvaluationResultDto:
    try:
        return await instrument.upload(command)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][instrument][handler] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
