import logging

from fastapi import APIRouter, Depends, Query

from titanic.adapter.inbound.api.deps.titanic_deps import get_walter_use_case
from titanic.adapter.inbound.api.schemas.titanic_schema import (
    WalterPassengerItem,
    WalterPassengerPageResponse,
)
from titanic.adapter.inbound.api.schemas.walter_schema import WalterSchema
from titanic.app.ports.input.walter_use_case import WalterUseCase

logger = logging.getLogger(__name__)
walter_router = APIRouter(prefix="/titanic/walter", tags=["walter"])


@walter_router.get("/passengers", response_model=WalterPassengerPageResponse)
async def read_walter_passengers(
    source_file: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=30, ge=1, le=100),
    walter: type[WalterUseCase] = Depends(get_walter_use_case),
) -> WalterPassengerPageResponse:
    schema = WalterSchema()
    logger.info("###############################################")
    logger.info("💊[월터 라우터] 월터의 자기소개글을 가져오는 API 호출")
    logger.info(f"👍🏻ID: {schema.id}")
    logger.info(f"🐥이름: {schema.name}")
    logger.info(f"🦜메모: {schema.memo}")
    logger.info("###############################################")
    result = await walter.read_passengers(source_file, page, size)
    response = WalterPassengerPageResponse(
        source_file=result.source_file,
        page=result.page,
        size=result.size,
        total=result.total,
        total_pages=result.total_pages,
        rows=[WalterPassengerItem(**row) for row in result.rows],
    )
    return response