from __future__ import annotations

from abc import ABC, abstractmethod

from star_craft.hub.domain.entities.hub_node import HubNode


class HubNodePort(ABC):
    """허브 노드 영속화 아웃바운드 Port."""

    @abstractmethod
    async def save(self, hub: HubNode) -> HubNode:
        ...

    @abstractmethod
    async def find_by_id(self, hub_id: int) -> HubNode | None:
        ...
