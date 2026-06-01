"""[Layer: Outbound] Hartley violin PG (스텁)."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.hartley_violin_repository_port import HartleyViolinRepositoryPort


class HartleyViolinPgRepository(HartleyViolinRepositoryPort):
    db: AsyncSession

    @staticmethod
    async def get_hartley_violin() -> dict[str, Any]:
        return {}
