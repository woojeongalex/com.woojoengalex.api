from __future__ import annotations

import logging

from star_craft.hub.app.dtos.spoke_dto import SpokeResult, TopologyResult
from star_craft.hub.app.ports.input.topology_query_use_case import TopologyQueryUseCase
from star_craft.hub.app.ports.output.hub_node_port import HubNodePort
from star_craft.hub.app.ports.output.spoke_registry_port import SpokeRegistryPort

logger = logging.getLogger("star_craft.hub.topology")


class TopologyQueryInteractor(TopologyQueryUseCase):
    """토폴로지 조회 Interactor."""

    def __init__(
        self,
        hub_node_port: HubNodePort,
        spoke_registry: SpokeRegistryPort,
    ) -> None:
        self._hub_node_port = hub_node_port
        self._spoke_registry = spoke_registry

    async def read_topology(self, hub_id: int) -> TopologyResult:
        logger.info("read topology | hub_id=%d", hub_id)
        hub = await self._hub_node_port.find_by_id(hub_id)
        if hub is None:
            raise ValueError(f"허브를 찾을 수 없음: {hub_id}")

        entries = await self._spoke_registry.find_all_by_hub(hub_id)
        spokes = [
            SpokeResult(
                id=e.id,
                spoke_name=e.spoke_name,
                domain_key=e.domain_key,
                endpoint_prefix=e.endpoint_prefix,
                status=e.status,
                tags=e.tags,
            )
            for e in entries
        ]
        return TopologyResult(
            hub_id=hub.id,
            hub_name=hub.name,
            spokes=spokes,
            total_spoke_count=len(spokes),
        )

    async def read_spoke(self, domain_key: str) -> SpokeResult:
        logger.info("read spoke | domain_key=%s", domain_key)
        entry = await self._spoke_registry.find_by_domain_key(domain_key)
        if entry is None:
            raise ValueError(f"스포크를 찾을 수 없음: {domain_key}")
        return SpokeResult(
            id=entry.id,
            spoke_name=entry.spoke_name,
            domain_key=entry.domain_key,
            endpoint_prefix=entry.endpoint_prefix,
            status=entry.status,
            tags=entry.tags,
        )
