import logging

from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.inbound.api.mappers.music_inbound_mapper import (
    from_evaluation_create,
    to_evaluation_response,
)
from music.adapter.inbound.api.schemas.sing_schema import (
    SingEvaluationCreateRequest,
    SingEvaluationResponse,
)
from music.adapter.outbound.pg.evaluation_pg_repository import EvaluationRepository
from music.adapter.outbound.pg.list_pg_repository import ListRepository
from music.app.ports.input.evaluation_use_case import EvaluationUseCase
from music.app.use_cases.evaluation_service import EvaluationService

logger = logging.getLogger(__name__)
evaluation_router = APIRouter(tags=["music-evaluation"])


def _use_case(db: AsyncSession) -> EvaluationUseCase:
    return EvaluationService(
        repository=EvaluationRepository(db),
        list_repository=ListRepository(db),
    )


@evaluation_router.post("/api/music/sing-evaluation", response_model=SingEvaluationResponse)
async def post_sing_evaluation(
    body: SingEvaluationCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> SingEvaluationResponse:
    logger.info(
        "[MUSIC][sing][1/router] POST /api/music/sing-evaluation input=%s",
        body.input_source,
    )
    try:
        result = await _use_case(db).save_evaluation(from_evaluation_create(body))
        return to_evaluation_response(result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][sing][1/router] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
