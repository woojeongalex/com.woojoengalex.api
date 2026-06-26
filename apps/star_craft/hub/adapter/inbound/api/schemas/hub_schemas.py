from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from star_craft.hub.domain.entities.spoke_registry import SpokeStatus


# ── Request ───────────────────────────────────────────────────

class RouteRequest(BaseModel):
    domain_key: str
    intent: str
    payload: dict[str, Any]
    request_id: str
    caller_id: str | None = None


class RegisterSpokeRequest(BaseModel):
    spoke_name: str
    domain_key: str
    endpoint_prefix: str
    tags: list[str] = []


# ── Response ──────────────────────────────────────────────────

class RouteResponse(BaseModel):
    routed_to: str
    result: dict[str, Any]
    request_id: str
    success: bool


class SpokeResponse(BaseModel):
    id: int
    spoke_name: str
    domain_key: str
    endpoint_prefix: str
    status: SpokeStatus
    tags: list[str]


class TopologyResponse(BaseModel):
    hub_id: int
    hub_name: str
    spokes: list[SpokeResponse]
    total_spoke_count: int
