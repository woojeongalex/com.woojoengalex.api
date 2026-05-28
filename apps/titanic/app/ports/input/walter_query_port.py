from typing import Protocol

from titanic.adapter.inbound.api.schemas.titanic_schema import WalterPassengerPageResponse


class WalterQueryPort(Protocol):
    """타이타닉 상세 조회 입력 포트."""

    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageResponse: ...
