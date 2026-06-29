from silicon_valley.app.dtos.piper_hendricks_ceo_dto import (
    HendricksCeoQuery,
    HendricksCeoResponse,
)
from silicon_valley.app.ports.output.piper_hendricks_ceo_port import HendricksCeoPort


class HendricksCeoRepository(HendricksCeoPort):
    async def introduce_myself(self, query: HendricksCeoQuery) -> HendricksCeoResponse:
        return HendricksCeoResponse(
            id=query.id,
            name=query.name,
            role="CEO / 파이드 파이퍼 창업자",
            description="천재 알고리즘 개발자. 사회성은 부족하지만 기술적 통찰력으로 파이드 파이퍼를 이끄는 인물.",
            ability="압축 알고리즘, 시스템 설계, 혁신적 문제 해결",
        )
