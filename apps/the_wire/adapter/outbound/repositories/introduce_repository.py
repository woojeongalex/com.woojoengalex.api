import logging

from the_wire.app.dtos.introduce_dto import IntroduceQuery, IntroduceResponse
from the_wire.app.ports.output.introduce_port import IntroducePort

logger = logging.getLogger(__name__)

_KO = IntroduceResponse(
    agent_name="The Wire",
    role="이메일 AI 에이전트",
    capabilities=[
        "이메일 초안 작성 및 발송",
        "수신자 주소록 관리",
        "Google 주소록 연동 및 로컬 저장",
        "CSV 연락처 일괄 업로드",
        "수신자 자동완성 검색",
    ],
    version="1.0.0",
)

_EN = IntroduceResponse(
    agent_name="The Wire",
    role="Email AI Agent",
    capabilities=[
        "Draft and send emails",
        "Manage contact address book",
        "Google Contacts sync with local storage",
        "Bulk CSV contact import",
        "Recipient autocomplete search",
    ],
    version="1.0.0",
)


class IntroduceRepository(IntroducePort):
    async def introduce_myself(self, query: IntroduceQuery) -> IntroduceResponse:
        logger.info(
            f"[IntroduceRepository] introduce_myself 진입 | locale={query.locale}"
        )
        return _KO if query.locale == "ko" else _EN
