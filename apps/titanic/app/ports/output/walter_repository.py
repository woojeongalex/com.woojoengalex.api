from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.titanic_schema import WalterPassengerPageResponse
from titanic.adapter.outbound.pg.walter_pg_repository import WalterPgRepository
from titanic.app.titanic_flow_log import titanic_flow_log


class WalterRepository:
    """출력 포트 구현 — PG 조회 어댑터로 위임."""

    def __init__(self, db: AsyncSession) -> None:
        self._pg_repository = WalterPgRepository(db)

    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageResponse:
        titanic_flow_log(
            "walter-read",
            "4/output",
            "to=outbound-pg source_file=%s page=%s size=%s",
            source_file or "latest",
            page,
            size,
        )
        return await self._pg_repository.read_passengers(source_file, page, size)
