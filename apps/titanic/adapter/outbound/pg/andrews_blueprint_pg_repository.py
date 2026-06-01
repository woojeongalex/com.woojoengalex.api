"""[Layer: Outbound] Andrews blueprint PG (스텁)."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.andrews_blueprint_repository_port import (
    AndrewsBlueprintRepositoryPort,
)


class AndrewsBlueprintPgRepository(AndrewsBlueprintRepositoryPort):
    db: AsyncSession

    @staticmethod
    async def get_andrews_blueprint() -> dict[str, Any]:
        return {}
