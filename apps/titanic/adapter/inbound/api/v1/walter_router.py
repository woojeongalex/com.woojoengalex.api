from fastapi import APIRouter, Depends, Query, Request

from titanic.adapter.inbound.api.deps.titanic_deps import get_walter_use_case
from titanic.adapter.inbound.api.mappers.passenger_mapper import passenger_page_dict_to_response
from titanic.adapter.inbound.api.schemas.titanic_schema import WalterPassengerPageResponse
from titanic.app.titanic_flow_log import titanic_flow_log
from titanic.app.ports.input.walter_use_case import WalterUseCase

walter_router = APIRouter(prefix="/titanic/walter", tags=["walter"])


@walter_router.get("/passengers", response_model=WalterPassengerPageResponse)
async def read_walter_passengers(
    request: Request,
    source_file: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=30, ge=1, le=100),
    walter: WalterUseCase = Depends(get_walter_use_case),
) -> WalterPassengerPageResponse:
    titanic_flow_log(
        "walter-read",
        "inbound",
        "origin=%s page=%s size=%s",
        request.headers.get("x-flow-origin", "unknown"),
        page,
        size,
        source_file=source_file or "latest",
    )
    passenger_page = await walter.read_passengers(source_file, page, size)
    return passenger_page_dict_to_response(passenger_page)
