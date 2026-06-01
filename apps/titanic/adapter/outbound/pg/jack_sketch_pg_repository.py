"""[Layer: Outbound] Jack sketch PG (스텁)."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.jack_sketch_repository_port import JackSketchRepositoryPort


class JackSketchPgRepository(JackSketchRepositoryPort):
    db: AsyncSession

    @staticmethod
    async def get_jack_sketch() -> dict[str, Any]:
        return {}
