"""[Layer: Outbound] Ruth corset PG (스텁)."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.ruth_corset_repository_port import RuthCorsetRepositoryPort


class RuthCorsetPgRepository(RuthCorsetRepositoryPort):
    db: AsyncSession

    @staticmethod
    async def get_ruth_corset() -> dict[str, Any]:
        return {}
