"""[Layer: Outbound] Smith captain PG (스텁)."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.smith_captain_repository_port import SmithCaptainRepositoryPort


class SmithCaptainPgRepository(SmithCaptainRepositoryPort):
    db: AsyncSession

    @staticmethod
    async def get_smith_captain() -> dict[str, Any]:
        return {}
