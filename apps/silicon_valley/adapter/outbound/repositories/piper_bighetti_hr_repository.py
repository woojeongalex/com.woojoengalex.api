from silicon_valley.app.dtos.piper_bighetti_hr_dto import (
    BighettiHrQuery,
    BighettiHrResponse,
)
from silicon_valley.app.ports.output.piper_bighetti_hr_port import BighettiHrPort


class BighettiHrRepository(BighettiHrPort):
    async def introduce_myself(self, query: BighettiHrQuery) -> BighettiHrResponse:
        return BighettiHrResponse(
            id=query.id,
            name=query.name,
            role="HR 담당 / 파이드 파이퍼 공동 창업자",
            description="리처드의 절친. 실력보다 운으로 Hooli에서 승승장구하다 HR을 담당하게 된 인물.",
            ability="인간관계, 운, 눈치 없는 낙천주의",
        )
