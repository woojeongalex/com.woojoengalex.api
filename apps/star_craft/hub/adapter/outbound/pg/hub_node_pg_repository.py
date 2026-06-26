from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from star_craft.hub.adapter.outbound.orm.hub_node_orm import HubNodeModel
from star_craft.hub.app.ports.output.hub_node_port import HubNodePort
from star_craft.hub.domain.entities.hub_node import HubNode


class HubNodePgRepository(HubNodePort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, hub: HubNode) -> HubNode:
        model = HubNodeModel(
            name=hub.name,
            description=hub.description,
            is_active=hub.is_active,
        )
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        hub.id = model.id
        return hub

    async def find_by_id(self, hub_id: int) -> HubNode | None:
        result = await self._session.execute(
            select(HubNodeModel).where(HubNodeModel.id == hub_id)
        )
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return HubNode(
            id=model.id,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
        )
