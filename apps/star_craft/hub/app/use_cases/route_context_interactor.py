from __future__ import annotations

import logging

from star_craft.hub.app.dtos.route_dto import RouteCommand, RouteResult
from star_craft.hub.app.ports.input.route_context_use_case import RouteContextUseCase
from star_craft.hub.app.ports.output.spoke_registry_port import SpokeRegistryPort

logger = logging.getLogger("star_craft.hub.route")


class RouteContextInteractor(RouteContextUseCase):
    """컨텍스트 라우팅 Interactor.

    도메인 키로 활성 스포크를 조회한 뒤 페이로드를 전달한다.
    스포크를 찾지 못하거나 비활성 상태면 ValueError를 발생시킨다.
    """

    def __init__(self, spoke_registry: SpokeRegistryPort) -> None:
        self._spoke_registry = spoke_registry

    async def route(self, command: RouteCommand) -> RouteResult:
        logger.info("route start | domain_key=%s intent=%s", command.domain_key, command.intent)

        spoke = await self._spoke_registry.find_by_domain_key(command.domain_key)
        if spoke is None:
            raise ValueError(f"등록되지 않은 스포크: {command.domain_key}")
        if not spoke.is_routable():
            raise ValueError(f"비활성 스포크: {command.domain_key} (status={spoke.status})")

        logger.info("route success | routed_to=%s", spoke.spoke_name)
        return RouteResult(
            routed_to=spoke.domain_key,
            result={"endpoint_prefix": spoke.endpoint_prefix, "payload": command.payload},
            request_id=command.request_id,
        )
