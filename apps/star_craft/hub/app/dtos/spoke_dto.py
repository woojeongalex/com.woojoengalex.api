from __future__ import annotations

from dataclasses import dataclass

from star_craft.hub.domain.entities.spoke_registry import SpokeStatus


@dataclass(frozen=True)
class RegisterSpokeCommand:
    """스포크 등록 Command DTO."""

    spoke_name: str
    domain_key: str
    endpoint_prefix: str
    tags: list[str]


@dataclass(frozen=True)
class SpokeResult:
    """스포크 조회/등록 결과 DTO."""

    id: int
    spoke_name: str
    domain_key: str
    endpoint_prefix: str
    status: SpokeStatus
    tags: list[str]


@dataclass(frozen=True)
class TopologyResult:
    """전체 토폴로지 조회 결과 DTO."""

    hub_id: int
    hub_name: str
    spokes: list[SpokeResult]
    total_spoke_count: int
