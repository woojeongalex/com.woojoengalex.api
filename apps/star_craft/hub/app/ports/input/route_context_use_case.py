from __future__ import annotations

from abc import ABC, abstractmethod

from star_craft.hub.app.dtos.route_dto import RouteCommand, RouteResult


class RouteContextUseCase(ABC):
    """컨텍스트 라우팅 인바운드 Port (ISP: 라우팅만 담당)."""

    @abstractmethod
    async def route(self, command: RouteCommand) -> RouteResult:
        """도메인 키와 인텐트를 기반으로 적절한 스포크에 라우팅한다."""
        ...
