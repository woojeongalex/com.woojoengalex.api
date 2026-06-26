from silicon_valley.app.dtos.piper_dunn_coo_dto import DunnCooQuery, DunnCooResponse
from silicon_valley.app.ports.output.piper_dunn_coo_port import DunnCooPort


class DunnCooRepository(DunnCooPort):
    async def introduce_myself(self, query: DunnCooQuery) -> DunnCooResponse:
        return DunnCooResponse(
            id=query.id,
            name=query.name,
            role="COO / 파이드 파이퍼",
            description="엔지니어 출신 COO. 비즈니스 감각과 기술 이해를 겸비한 현실적인 관리자.",
            ability="사업 운영, 협상, 팀 조율",
        )
