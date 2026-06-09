from typing import Any

from titanic.app.dtos.crew_walter_query import WalterPassengerPageDto
from titanic.app.ports.input.crew_walter_use_case import WalterUseCase
from titanic.app.ports.output.crew_walter_director_repository import WalterDirectorRepository


class WalterInteractor(WalterUseCase):

    def __init__(self, repository: WalterDirectorRepository) -> None:
        self._repository = repository

    async def introduce_myself(self) -> dict[str, Any]:
        return {
            "id": 6,
            "name": "Walter Lord",
            "role": "역사가 · 승객 기록 조회 담당",
            "description": (
                "타이타닉 침몰의 역사를 기록한 역사가. "
                "승객 데이터를 조회하고 기록을 보존하는 일을 맡고 있습니다."
            ),
            "ability": "승객 목록 페이지네이션 조회",
            "book": "A Night to Remember (1955)",
        }

    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageDto:
        return await self._repository.read_passengers(source_file, page, size)