from __future__ import annotations

import logging

from star_craft.hub.app.dtos.spoke_dto import RegisterSpokeCommand, SpokeResult
from star_craft.hub.app.ports.input.register_spoke_use_case import RegisterSpokeUseCase
from star_craft.hub.app.ports.output.spoke_registry_port import SpokeRegistryPort
from star_craft.hub.domain.entities.spoke_registry import SpokeRegistryEntry, SpokeStatus

logger = logging.getLogger("star_craft.hub.register")


class RegisterSpokeInteractor(RegisterSpokeUseCase):
    """스포크 등록 Interactor."""

    def __init__(self, spoke_registry: SpokeRegistryPort) -> None:
        self._spoke_registry = spoke_registry

    async def register(self, command: RegisterSpokeCommand) -> SpokeResult:
        logger.info("register spoke | domain_key=%s", command.domain_key)

        existing = await self._spoke_registry.find_by_domain_key(command.domain_key)
        if existing is not None:
            raise ValueError(f"이미 등록된 domain_key: {command.domain_key}")

        entry = SpokeRegistryEntry(
            id=0,  # DB가 할당
            spoke_name=command.spoke_name,
            domain_key=command.domain_key,
            endpoint_prefix=command.endpoint_prefix,
            status=SpokeStatus.ACTIVE,
            tags=list(command.tags),
        )
        saved = await self._spoke_registry.save(entry)
        logger.info("register spoke success | id=%d", saved.id)

        return SpokeResult(
            id=saved.id,
            spoke_name=saved.spoke_name,
            domain_key=saved.domain_key,
            endpoint_prefix=saved.endpoint_prefix,
            status=saved.status,
            tags=saved.tags,
        )
