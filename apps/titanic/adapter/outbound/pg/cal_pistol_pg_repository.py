"""[Layer: Outbound] Cal pistol PG (스텁)."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.ports.output.cal_pistol_repository_port import CalPistolRepositoryPort


class CalPistolPgRepository(CalPistolRepositoryPort):
    db: AsyncSession

    @staticmethod
    async def get_cal_pistol() -> dict[str, Any]:
        return {}
