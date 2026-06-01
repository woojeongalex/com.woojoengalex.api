from fastapi import APIRouter, Depends, Query, Request

from titanic.adapter.inbound.api.deps.titanic_deps import get_walter_use_case
from titanic.adapter.inbound.api.handlers.titanic_inbound_handlers import handle_walter_read
from titanic.adapter.inbound.api.schemas.titanic_schema import WalterPassengerPageResponse
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
    return await handle_walter_read(request, source_file, page, size, walter)
