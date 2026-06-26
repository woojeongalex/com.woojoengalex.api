from silicon_valley.app.dtos.piper_gilfoyle_system_dto import GilfoyleSystemQuery, GilfoyleSystemResponse
from silicon_valley.app.ports.output.piper_gilfoyle_system_port import GilfoyleSystemPort


class GilfoyleSystemRepository(GilfoyleSystemPort):
    async def introduce_myself(self, query: GilfoyleSystemQuery) -> GilfoyleSystemResponse:
        return GilfoyleSystemResponse(
            id=query.id,
            name=query.name,
            role="시스템 아키텍트 / 파이드 파이퍼",
            description="냉소적이고 자만심 강한 시스템 전문가. 보안과 인프라에 탁월하며 디네시와 늘 티격태격.",
            ability="시스템 설계, 보안, 서버 인프라, 리눅스",
        )
