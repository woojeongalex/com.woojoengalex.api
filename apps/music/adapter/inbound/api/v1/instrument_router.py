import logging

from database import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.inbound.api.mappers.music_inbound_mapper import (
    from_instrument_create,
    to_instrument_catalog_response,
    to_instrument_response,
)
from music.adapter.inbound.api.schemas.instrument_schemas import (
    InstrumentCatalogResponse,
    InstrumentEvaluationCreateRequest,
    InstrumentEvaluationResponse,
)
from music.adapter.outbound.pg.instrument_pg_repository import InstrumentRepository
from music.app.ports.input.instrument_use_case import InstrumentUseCase
from music.app.use_cases.instrument_service import InstrumentService

logger = logging.getLogger(__name__)
instrument_router = APIRouter(tags=["music-instrument"])


def _interactor(db: AsyncSession | None) -> InstrumentUseCase:
    return InstrumentService(InstrumentRepository(db))


@instrument_router.get("/api/music/instrument-catalog", response_model=InstrumentCatalogResponse)
async def get_instrument_catalog(
    q: str = Query("", description="악기 검색어"),
) -> InstrumentCatalogResponse:
    return to_instrument_catalog_response(_interactor(None).list_catalog(q))


@instrument_router.post(
    "/api/music/instrument-evaluation",
    response_model=InstrumentEvaluationResponse,
)
async def post_instrument_evaluation(
    body: InstrumentEvaluationCreateRequest,
    db: AsyncSession = Depends(get_db),
) -> InstrumentEvaluationResponse:
    try:
        result = await _interactor(db).save_evaluation(from_instrument_create(body))
        return to_instrument_response(result)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("[MUSIC][instrument] DB 오류: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
