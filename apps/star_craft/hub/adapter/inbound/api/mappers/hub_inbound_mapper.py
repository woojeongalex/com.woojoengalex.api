from __future__ import annotations

from star_craft.hub.adapter.inbound.api.schemas.hub_schemas import (
    RegisterSpokeRequest,
    RouteRequest,
    RouteResponse,
    SpokeResponse,
    TopologyResponse,
)
from star_craft.hub.app.dtos.route_dto import RouteCommand, RouteResult
from star_craft.hub.app.dtos.spoke_dto import RegisterSpokeCommand, SpokeResult, TopologyResult


def route_request_to_command(req: RouteRequest) -> RouteCommand:
    return RouteCommand(
        domain_key=req.domain_key,
        intent=req.intent,
        payload=req.payload,
        request_id=req.request_id,
        caller_id=req.caller_id,
    )


def route_result_to_response(result: RouteResult) -> RouteResponse:
    return RouteResponse(
        routed_to=result.routed_to,
        result=result.result,
        request_id=result.request_id,
        success=result.success,
    )


def register_spoke_request_to_command(req: RegisterSpokeRequest) -> RegisterSpokeCommand:
    return RegisterSpokeCommand(
        spoke_name=req.spoke_name,
        domain_key=req.domain_key,
        endpoint_prefix=req.endpoint_prefix,
        tags=req.tags,
    )


def spoke_result_to_response(result: SpokeResult) -> SpokeResponse:
    return SpokeResponse(
        id=result.id,
        spoke_name=result.spoke_name,
        domain_key=result.domain_key,
        endpoint_prefix=result.endpoint_prefix,
        status=result.status,
        tags=result.tags,
    )


def topology_result_to_response(result: TopologyResult) -> TopologyResponse:
    return TopologyResponse(
        hub_id=result.hub_id,
        hub_name=result.hub_name,
        spokes=[spoke_result_to_response(s) for s in result.spokes],
        total_spoke_count=result.total_spoke_count,
    )
