from __future__ import annotations

from abc import ABC, abstractmethod

from star_craft.hub.app.dtos.spoke_dto import RegisterSpokeCommand, SpokeResult


class RegisterSpokeUseCase(ABC):
    """스포크 등록 인바운드 Port (ISP: 등록만 담당)."""

    @abstractmethod
    async def register(self, command: RegisterSpokeCommand) -> SpokeResult:
        """새 스포크를 허브 레지스트리에 등록한다."""
        ...
