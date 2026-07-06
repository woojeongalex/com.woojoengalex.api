from datetime import datetime
import logging

from the_wire.app.dtos.introduce_dto import IntroduceQuery, IntroduceResponse
from the_wire.app.dtos.judge_dto import JudgeCommand, JudgeResult
from the_wire.app.ports.input.judge_use_case import JudgeUseCase
from the_wire.app.ports.output.judge_repository_port import JudgeRepositoryPort
from the_wire.domain.entities.judge import Verdict

logger = logging.getLogger(__name__)

_ESCALATION_KEYWORDS = ("보고서", "실적", "긴급", "report", "erp", "에스컬레이션")

_INTRODUCE_KO = IntroduceResponse(
    agent_name="Judge (Watson Triage)",
    role="인바운드 이메일 분류 및 라우팅 판정관",
    capabilities=[
        "발신자 중요도(VIP 여부) 분류",
        "본문 키워드 기반 에스컬레이션 판정",
        "Case A (일반) → InboxInteractor 종결",
        "Case B (VIP/보고서) → StarCraft → FakerOrchestrator 에스컬레이션",
        "판정 이력 pgvector 저장",
    ],
    version="1.0.0",
)

_INTRODUCE_EN = IntroduceResponse(
    agent_name="Judge (Watson Triage)",
    role="Inbound Email Triage & Routing Judge",
    capabilities=[
        "Classify sender importance (VIP detection)",
        "Keyword-based escalation verdict",
        "Case A (normal) → InboxInteractor resolution",
        "Case B (VIP/report) → StarCraft → FakerOrchestrator escalation",
        "Persist verdict history to pgvector",
    ],
    version="1.0.0",
)


class JudgeInteractor(JudgeUseCase):
    def __init__(self, repository: JudgeRepositoryPort) -> None:
        self._repository = repository

    def judge(self, command: JudgeCommand) -> JudgeResult:
        logger.info("[JudgeInteractor] judge | sender=%s", command.sender)
        verdict, reason = self._triage(command)
        result = JudgeResult(
            verdict=verdict.value,
            sender=command.sender,
            subject=command.subject,
            reason=reason,
            judged_at=datetime.utcnow(),
        )
        logger.info("[JudgeInteractor] verdict=%s | reason=%s", verdict.value, reason)
        return result

    async def introduce_myself(self, query: IntroduceQuery) -> IntroduceResponse:
        logger.info("[JudgeInteractor] introduce_myself | locale=%s", query.locale)
        return _INTRODUCE_KO if query.locale == "ko" else _INTRODUCE_EN

    def _triage(self, command: JudgeCommand) -> tuple[Verdict, str]:
        if command.important_client:
            return Verdict.CASE_B, "VIP 거래처 — 자동 에스컬레이션"
        combined = f"{command.subject} {command.body}".lower()
        hit = next((kw for kw in _ESCALATION_KEYWORDS if kw in combined), None)
        if hit:
            return Verdict.CASE_B, f"에스컬레이션 키워드 감지: '{hit}'"
        return Verdict.CASE_A, "일반 업무 — Holmes 자체 종결"
