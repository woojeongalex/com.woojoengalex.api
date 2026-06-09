"""[Layer: Use Cases] Hartley violin (HartleyViolinUseCase 구현)."""

from dataclasses import asdict
from typing import Any

from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.output.crew_hartley_violin_repository import HartleyViolinRepository


class HartleyViolinInteractor(HartleyViolinUseCase):
    def __init__(self, repository: HartleyViolinRepository) -> None:
        self._repository = repository

    async def introduce_myself(self) -> dict[str, Any]:
        query = HartleyViolinQuery(id=3, name="월레스 하틀리 (Wallace Hartley)")
        response = await self._repository.introduce_myself(query)
        return asdict(response)
