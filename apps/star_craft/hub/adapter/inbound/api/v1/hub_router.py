from __future__ import annotations

from fastapi import APIRouter, Depends

from star_craft.hub.adapter.inbound.api.deps.hub_deps import (
    get_register_spoke_use_case,
    get_route_context_use_case,
    get_topology_query_use_case,
)
from star_craft.hub.adapter.inbound.api.handlers.hub_inbound_handlers import handle_hub_errors
from star_craft.hub.adapter.inbound.api.mappers.hub_inbound_mapper import (
    register_spoke_request_to_command,
    route_request_to_command,
    route_result_to_response,
    spoke_result_to_response,
    topology_result_to_response,
)
from star_craft.hub.adapter.inbound.api.schemas.hub_schemas import (
    RegisterSpokeRequest,
    RouteRequest,
    RouteResponse,
    SpokeResponse,
    TopologyResponse,
)
from star_craft.hub.app.ports.input.register_spoke_use_case import RegisterSpokeUseCase
from star_craft.hub.app.ports.input.route_context_use_case import RouteContextUseCase
from star_craft.hub.app.ports.input.topology_query_use_case import TopologyQueryUseCase

hub_router = APIRouter(prefix="/api/hub", tags=["hub"])


@hub_router.post("/route", response_model=RouteResponse)
async def route_context(
    body: RouteRequest,
    use_case: RouteContextUseCase = Depends(get_route_context_use_case),
) -> RouteResponse:
    try:
        result = await use_case.route(route_request_to_command(body))
        return route_result_to_response(result)
    except Exception as exc:
        handle_hub_errors(exc)


@hub_router.post("/spokes", response_model=SpokeResponse, status_code=201)
async def register_spoke(
    body: RegisterSpokeRequest,
    use_case: RegisterSpokeUseCase = Depends(get_register_spoke_use_case),
) -> SpokeResponse:
    try:
        result = await use_case.register(register_spoke_request_to_command(body))
        return spoke_result_to_response(result)
    except Exception as exc:
        handle_hub_errors(exc)


@hub_router.get("/topology/{hub_id}", response_model=TopologyResponse)
async def read_topology(
    hub_id: int,
    use_case: TopologyQueryUseCase = Depends(get_topology_query_use_case),
) -> TopologyResponse:
    try:
        result = await use_case.read_topology(hub_id)
        return topology_result_to_response(result)
    except Exception as exc:
        handle_hub_errors(exc)


@hub_router.get("/spokes/{domain_key}", response_model=SpokeResponse)
async def read_spoke(
    domain_key: str,
    use_case: TopologyQueryUseCase = Depends(get_topology_query_use_case),
) -> SpokeResponse:
    try:
        result = await use_case.read_spoke(domain_key)
        return spoke_result_to_response(result)
    except Exception as exc:
        handle_hub_errors(exc)
