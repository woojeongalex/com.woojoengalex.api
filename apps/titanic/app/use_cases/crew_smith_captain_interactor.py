"""[Layer: Use Cases] Smith captain (SmithCaptainUseCase 구현)."""

from typing import Any

from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository


class SmithCaptainInteractor(SmithCaptainUseCase):
    def __init__(self, repository: SmithCaptainRepository) -> None:
        self._repository = repository

    async def introduce_myself(self) -> dict[str, Any]:
        return {
            "id": 2,
            "name": "에드워드 존 스미스 (Captain Edward John Smith)",
            "role": "선장 · 항해 총괄",
            "description": (
                "타이타닉의 마지막 항해를 지휘한 선장. "
                "침몰 순간까지 배와 함께하며 승객 대피를 진두지휘했습니다."
            ),
            "ability": "운항 총괄 지휘",
            "class": "승무원",
        }
