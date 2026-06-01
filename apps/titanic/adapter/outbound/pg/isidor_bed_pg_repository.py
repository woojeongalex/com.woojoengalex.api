"""[Layer: Outbound] Isidor bed PG (스텁)."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.isidor_bed_repository_port import IsidorBedRepositoryPort


class IsidorBedPgRepository(IsidorBedRepositoryPort):
    db: AsyncSession

    @staticmethod
    async def get_isidor_bed() -> dict[str, Any]:
        return {}
