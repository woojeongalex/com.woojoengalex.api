from silicon_valley.app.dtos.piper_dinesh_dash_dto import DineshDashQuery, DineshDashResponse
from silicon_valley.app.ports.output.piper_dinesh_dash_port import DineshDashPort


class DineshDashRepository(DineshDashPort):
    async def introduce_myself(self, query: DineshDashQuery) -> DineshDashResponse:
        return DineshDashResponse(
            id=query.id,
            name=query.name,
            role="백엔드 엔지니어 / 파이드 파이퍼",
            description="길포일의 라이벌. 자존심 강하고 코딩 실력을 항상 과시하려 하는 인물.",
            ability="백엔드 개발, 경쟁심, 빠른 코딩 속도",
        )
