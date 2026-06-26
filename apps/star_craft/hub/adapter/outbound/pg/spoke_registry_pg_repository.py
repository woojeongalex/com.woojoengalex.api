from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from star_craft.hub.adapter.outbound.orm.spoke_registry_orm import SpokeRegistryModel
from star_craft.hub.app.ports.output.spoke_registry_port import SpokeRegistryPort
from star_craft.hub.domain.entities.spoke_registry import SpokeRegistryEntry, SpokeStatus


class SpokeRegistryPgRepository(SpokeRegistryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, entry: SpokeRegistryEntry) -> SpokeRegistryEntry:
        model = SpokeRegistryModel(
            spoke_name=entry.spoke_name,
            domain_key=entry.domain_key,
            endpoint_prefix=entry.endpoint_prefix,
            status=entry.status,
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        entry.id = model.id
        return entry

    async def find_by_domain_key(self, domain_key: str) -> SpokeRegistryEntry | None:
        result = await self._session.execute(
            select(SpokeRegistryModel).where(SpokeRegistryModel.domain_key == domain_key)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_entity(model)

    async def find_all_by_hub(self, hub_id: int) -> list[SpokeRegistryEntry]:
        result = await self._session.execute(
            select(SpokeRegistryModel).where(SpokeRegistryModel.hub_id == hub_id)
        )
        return [self._to_entity(m) for m in result.scalars().all()]

    async def delete(self, spoke_id: int) -> None:
        result = await self._session.execute(
            select(SpokeRegistryModel).where(SpokeRegistryModel.id == spoke_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.commit()

    def _to_entity(self, model: SpokeRegistryModel) -> SpokeRegistryEntry:
        return SpokeRegistryEntry(
            id=model.id,
            spoke_name=model.spoke_name,
            domain_key=model.domain_key,
            endpoint_prefix=model.endpoint_prefix,
            status=SpokeStatus(model.status),
        )
