from __future__ import annotations

from abc import ABC, abstractmethod

from star_craft.hub.app.dtos.spoke_dto import SpokeResult, TopologyResult


class TopologyQueryUseCase(ABC):
    """토폴로지 조회 인바운드 Port (ISP: 읽기만 담당)."""

    @abstractmethod
    async def read_topology(self, hub_id: int) -> TopologyResult:
        """허브에 연결된 전체 스포크 토폴로지를 반환한다."""
        ...

    @abstractmethod
    async def read_spoke(self, domain_key: str) -> SpokeResult:
        """도메인 키로 특정 스포크 정보를 조회한다."""
        ...
