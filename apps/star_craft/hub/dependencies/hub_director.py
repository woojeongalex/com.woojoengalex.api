from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from star_craft.hub.adapter.outbound.pg.hub_node_pg_repository import HubNodePgRepository
from star_craft.hub.adapter.outbound.pg.spoke_registry_pg_repository import (
    SpokeRegistryPgRepository,
)
from star_craft.hub.app.ports.input.register_spoke_use_case import RegisterSpokeUseCase
from star_craft.hub.app.ports.input.route_context_use_case import RouteContextUseCase
from star_craft.hub.app.ports.input.topology_query_use_case import TopologyQueryUseCase
from star_craft.hub.app.ports.output.hub_node_port import HubNodePort
from star_craft.hub.app.ports.output.spoke_registry_port import SpokeRegistryPort
from star_craft.hub.app.use_cases.register_spoke_interactor import RegisterSpokeInteractor
from star_craft.hub.app.use_cases.route_context_interactor import RouteContextInteractor
from star_craft.hub.app.use_cases.topology_query_interactor import TopologyQueryInteractor


# ── Repository (outbound) ─────────────────────────────────────

def get_spoke_registry_repository(
    db: AsyncSession = Depends(get_db),
) -> SpokeRegistryPort:
    return SpokeRegistryPgRepository(session=db)


def get_hub_node_repository(
    db: AsyncSession = Depends(get_db),
) -> HubNodePort:
    return HubNodePgRepository(session=db)


# ── Use Case (inbound) ────────────────────────────────────────

def get_route_context_use_case(
    spoke_registry: SpokeRegistryPort = Depends(get_spoke_registry_repository),
) -> RouteContextUseCase:
    return RouteContextInteractor(spoke_registry=spoke_registry)


def get_register_spoke_use_case(
    spoke_registry: SpokeRegistryPort = Depends(get_spoke_registry_repository),
) -> RegisterSpokeUseCase:
    return RegisterSpokeInteractor(spoke_registry=spoke_registry)


def get_topology_query_use_case(
    hub_node_port: HubNodePort = Depends(get_hub_node_repository),
    spoke_registry: SpokeRegistryPort = Depends(get_spoke_registry_repository),
) -> TopologyQueryUseCase:
    return TopologyQueryInteractor(
        hub_node_port=hub_node_port,
        spoke_registry=spoke_registry,
    )
