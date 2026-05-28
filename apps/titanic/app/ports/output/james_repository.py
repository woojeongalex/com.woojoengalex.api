from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.titanic_request import TitanicCommandRequest
from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic.app.titanic_flow_log import titanic_flow_log


class JamesRepository:
    """출력 포트 구현 — PG 어댑터로 위임."""

    def __init__(self, db: AsyncSession) -> None:
        self._pg_repository = JamesPgRepository(db)

    async def move_uploaded_rows(
        self,
        file_name: str,
        rows: list[TitanicCommandRequest],
    ) -> dict[str, object]:
        titanic_flow_log(
            "james-upload",
            "4/output",
            "to=outbound-pg file=%s rows=%s",
            file_name,
            len(rows),
        )
        return await self._pg_repository.move_uploaded_rows(file_name, rows)
