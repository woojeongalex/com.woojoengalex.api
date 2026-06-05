import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from music.app.dtos.speech_dto import SpeechEvaluationCreateCommand, SpeechEvaluationResultDto
from music.app.ports.input.speech_use_case import SpeechUseCase

logger = logging.getLogger(__name__)


async def pass_speech_evaluation(
    speech: SpeechUseCase,
    command: SpeechEvaluationCreateCommand,
) -> SpeechEvaluationResultDto:
    try:
        return await speech.upload(command)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][speech][handler] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
