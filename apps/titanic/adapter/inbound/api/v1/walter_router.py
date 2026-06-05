from fastapi import APIRouter, Depends, Query

from titanic.adapter.inbound.api.deps.titanic_deps import get_walter_use_case
from titanic.adapter.inbound.api.mappers.walter_inbound_mapper import (
    walter_page_dto_to_response,
)
from titanic.adapter.inbound.api.schemas.titanic_schema import WalterPassengerPageResponse
from titanic.adapter.inbound.api.schemas.walter_schema import WalterSchema
from titanic.app.dtos.walter_query import WalterResponse
from titanic.app.ports.input.walter_use_case import WalterUseCase

walter_router = APIRouter(prefix="/titanic/walter", tags=["walter"])


@walter_router.get("/myself")
async def introduce_myself(
    walter: WalterUseCase = Depends(get_walter_use_case),
) -> WalterResponse:
    return await walter.introduce_myself(
        WalterSchema(
            id=2,
            name="Walter Nichols",
            memo="타이타닉 탑승자 데이터 분석",
        )
    )


@walter_router.get("/passengers", response_model=WalterPassengerPageResponse)
async def read_passengers(
    source_file: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    walter: WalterUseCase = Depends(get_walter_use_case),
) -> WalterPassengerPageResponse:
    page_dto = await walter.read_passengers(source_file, page, size)
    return walter_page_dto_to_response(page_dto)
