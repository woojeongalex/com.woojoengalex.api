from fastapi import APIRouter, Depends, Query, Request

from titanic.adapter.inbound.api.schemas.titanic_schema import WalterPassengerPageResponse
from titanic.app.ports.input.walter_query_port import WalterQueryPort
from titanic.app.titanic_flow_log import titanic_flow_log
from titanic.app.use_cases.walter_query import get_walter_query

walter_router = APIRouter(prefix="/titanic/walter", tags=["walter"])


@walter_router.get("/passengers", response_model=WalterPassengerPageResponse)
async def read_walter_passengers(
    request: Request,
    source_file: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=30, ge=1, le=100),
    query: WalterQueryPort = Depends(get_walter_query),
) -> WalterPassengerPageResponse:
    origin = request.headers.get("x-flow-origin", "unknown")
    titanic_flow_log(
        "walter-read",
        "1/frontend->inbound",
        "origin=%s source_file=%s",
        origin,
        source_file or "latest",
    )
    titanic_flow_log(
        "walter-read",
        "1/inbound",
        "request page=%s size=%s to=input-port",
        page,
        size,
    )
    result = await query.read_passengers(source_file, page, size)
    titanic_flow_log(
        "walter-read",
        "1/inbound",
        "response rows=%s total=%s to=frontend",
        len(result.rows),
        result.total,
    )
    return result
