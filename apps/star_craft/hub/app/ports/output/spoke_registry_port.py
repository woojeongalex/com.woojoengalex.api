from __future__ import annotations

from abc import ABC, abstractmethod

from star_craft.hub.domain.entities.spoke_registry import SpokeRegistryEntry


class SpokeRegistryPort(ABC):
    """스포크 레지스트리 아웃바운드 Port."""

    @abstractmethod
    async def save(self, entry: SpokeRegistryEntry) -> SpokeRegistryEntry:
        ...

    @abstractmethod
    async def find_by_domain_key(self, domain_key: str) -> SpokeRegistryEntry | None:
        ...

    @abstractmethod
    async def find_all_by_hub(self, hub_id: int) -> list[SpokeRegistryEntry]:
        ...

    @abstractmethod
    async def delete(self, spoke_id: int) -> None:
        ...
