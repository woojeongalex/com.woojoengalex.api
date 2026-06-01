"""[Layer: Outbound] Rose PG — 데이터셋 스키마 (스텁)."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.rose_repository_port import RoseRepositoryPort


class RosePgRepository(RoseRepositoryPort):
    db: AsyncSession

    @staticmethod
    async def read_titanic_schema() -> dict[str, Any]:
        return {}
