"""
Watson Test Harness
===================
watcher-policy.md 스펙을 기반으로 한 멀티 에이전트 라우팅 검증 하네스.

실행:
    cd woojeongai
    python -m apps.the_wire._docs.harness.watson_test_harness
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import textwrap
from typing import Any

# ──────────────────────────────────────────────
# 0. 내러티브 로거
# ──────────────────────────────────────────────

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
GRAY = "\033[90m"
MAGENTA = "\033[95m"


def _ts() -> str:
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


def log(level: str, agent: str, msg: str, color: str = RESET) -> None:
    tag = f"{color}[{level}]{RESET}"
    print(f"  {GRAY}{_ts()}{RESET} {tag} {BOLD}{agent}{RESET} — {msg}")


def divider(title: str) -> None:
    width = 64
    bar = "-" * width
    print(f"\n{CYAN}{bar}{RESET}")
    print(f"{CYAN}  {title}{RESET}")
    print(f"{CYAN}{bar}{RESET}\n")


# ──────────────────────────────────────────────
# 1. 가상 이벤트 (Mock Inbound Event)
# ──────────────────────────────────────────────


class Priority(str, Enum):
    NORMAL = "NORMAL"
    VIP = "VIP"


@dataclass
class InboundMailEvent:
    """police_lestrade_telegram / police_anderson_discord 등이 전달하는 raw 이벤트."""

    sender: str
    subject: str
    body: str
    important_client: bool = False
    channel: str = "gmail"
    received_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def priority(self) -> Priority:
        return Priority.VIP if self.important_client else Priority.NORMAL


# ──────────────────────────────────────────────
# 2. Mock 이벤트 생성기
# ──────────────────────────────────────────────


def build_scenario_1() -> InboundMailEvent:
    """Scenario 1 — 일반 거래처 단순 인사 메일."""
    return InboundMailEvent(
        sender="general.partner@example.com",
        subject="안녕하세요, 간단한 문의드립니다",
        body="안녕하세요. 저희 회사는 귀사의 서비스에 관심이 있어 간단히 문의드립니다. 편하실 때 답변 부탁드립니다.",
        important_client=False,
        channel="gmail",
    )


def build_scenario_2() -> InboundMailEvent:
    """Scenario 2 — VIP 거래처 분기 보고서 에스컬레이션 요청."""
    return InboundMailEvent(
        sender="vip.ceo@bigcorp.co.kr",
        subject="[긴급] 2025 Q2 분기 실적 자동 보고서 발행 요망",
        body=(
            "안녕하세요. 이번 2분기 실적을 분기 보고서로 자동 발행해 주시기 바랍니다. "
            "전사 ERP 데이터를 취합하여 임원진에게 공유될 수 있도록 페이커 에이전트를 통한 "
            "최종 보고서 생성을 요청드립니다."
        ),
        important_client=True,
        channel="gmail",
    )


# ──────────────────────────────────────────────
# 3. Holmes — 일반 처리 에이전트 (Mock)
# ──────────────────────────────────────────────


class MockHolmesInteractor:
    """the_wire/app/use_cases/inbox_interactor.py 의 InboxInteractor 를 모사."""

    async def receive(self, event: InboundMailEvent) -> dict[str, Any]:
        log(
            "HOLMES",
            "InboxInteractor",
            f"수신 처리 시작 | sender={event.sender}",
            GREEN,
        )
        await asyncio.sleep(0.05)  # I/O 모사
        log("HOLMES", "InboxInteractor", "pgvector 임베딩 생성 중…", GREEN)
        await asyncio.sleep(0.1)
        log("HOLMES", "InboxInteractor", "wire_inbox 테이블 저장 완료 ✓", GREEN)
        return {
            "status": "resolved",
            "handler": "Holmes/InboxInteractor",
            "sender": event.sender,
            "subject": event.subject,
        }


# ──────────────────────────────────────────────
# 4. StarCraft 온톨로지 버스 (Mock Event Bus)
# ──────────────────────────────────────────────


class MockStarCraftBus:
    """star_craft/ 온톨로지 허브를 모사하는 이벤트 버스."""

    async def publish(self, event: InboundMailEvent) -> dict[str, Any]:
        log("STAR_CRAFT", "OntologyBus", f"이벤트 수신 | sender={event.sender}", YELLOW)
        await asyncio.sleep(0.05)
        log("STAR_CRAFT", "OntologyBus", "전사 컨텍스트 인덱싱 중…", YELLOW)
        await asyncio.sleep(0.05)
        log(
            "STAR_CRAFT", "OntologyBus", "FakerOrchestrator 에스컬레이션 발행 ▶", YELLOW
        )
        return {
            "bus": "star_craft",
            "escalated_to": "FakerOrchestrator",
            "payload": {
                "sender": event.sender,
                "subject": event.subject,
                "body": event.body,
            },
        }


# ──────────────────────────────────────────────
# 5. Faker — 최고 사령탑 (Mock)
# ──────────────────────────────────────────────


class MockFakerOrchestrator:
    """core/lol/t1_mid_faker_orchestrator.py 의 FakerOrchestrator 를 모사.
    실제 EXAONE 호출 없이 보고서 생성 흐름만 검증한다.
    """

    async def wake_up(self, escalation: dict[str, Any]) -> dict[str, Any]:
        payload = escalation["payload"]
        log("FAKER", "FakerOrchestrator", "⚡ Wake-up 수신 — EXAONE 활성화", MAGENTA)
        await asyncio.sleep(0.1)
        log(
            "FAKER",
            "FakerOrchestrator",
            "전사 ERP 데이터 취합 중 (titanic / silicon_valley)…",
            MAGENTA,
        )
        await asyncio.sleep(0.15)
        report = (
            f"[EXAONE 보고서]\n"
            f"수신자: {payload['sender']}\n"
            f"제목: {payload['subject']}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"2025 Q2 분기 실적 자동 보고서가 생성되었습니다.\n"
            f"(실제 환경에서는 EXAONE 3.5 모델이 ERP 데이터를 취합하여 작성)"
        )
        log("FAKER", "FakerOrchestrator", "최종 보고서 생성 완료 ✓", MAGENTA)
        return {
            "status": "escalated_and_resolved",
            "handler": "FakerOrchestrator/EXAONE",
            "report": report,
        }


# ──────────────────────────────────────────────
# 6. Watson — Triage Nurse / 라우팅 인터셉터
# ──────────────────────────────────────────────

_ESCALATION_KEYWORDS = ("보고서", "실적", "긴급", "report", "ERP", "에스컬레이션")


class WatsonWatcherHub:
    """
    the_wire/adapter/inbound/api/v1/inbox_router.py 앞단에서
    인바운드 이벤트를 가로채 라우팅 결정을 내리는 게이트웨이.

    Routing Rules
    ─────────────
    Case A — 일반  : InboxInteractor (Holmes) 에서 자체 종결
    Case B — VIP   : StarCraft 온톨로지 버스 → FakerOrchestrator 에스컬레이션
    """

    def __init__(self) -> None:
        self._holmes = MockHolmesInteractor()
        self._star_craft = MockStarCraftBus()
        self._faker = MockFakerOrchestrator()

    def _is_escalation(self, event: InboundMailEvent) -> bool:
        if event.important_client:
            return True
        combined = f"{event.subject} {event.body}".lower()
        return any(kw.lower() in combined for kw in _ESCALATION_KEYWORDS)

    async def intercept(self, event: InboundMailEvent) -> dict[str, Any]:
        log(
            "WATSON",
            "WatcherHub",
            f"이벤트 수신 | channel={event.channel} priority={event.priority.value}",
            CYAN,
        )
        log("WATSON", "WatcherHub", f"발신자: {event.sender}", CYAN)
        log("WATSON", "WatcherHub", f"제목: {event.subject}", CYAN)

        if self._is_escalation(event):
            log(
                "WATSON",
                "WatcherHub",
                "🔴 TRIAGE → Case B (VIP/에스컬레이션) 판정",
                RED,
            )
            escalation = await self._star_craft.publish(event)
            result = await self._faker.wake_up(escalation)
        else:
            log("WATSON", "WatcherHub", "🟢 TRIAGE → Case A (일반 업무) 판정", GREEN)
            result = await self._holmes.receive(event)

        return result


# ──────────────────────────────────────────────
# 7. 하네스 러너
# ──────────────────────────────────────────────


async def run_harness() -> None:
    watson = WatsonWatcherHub()
    scenarios = [
        ("Scenario 1 — 일반 거래처 단순 문의", build_scenario_1()),
        ("Scenario 2 — VIP 분기 보고서 에스컬레이션", build_scenario_2()),
    ]

    print(f"\n{BOLD}{'=' * 66}{RESET}")
    print(f"{BOLD}  Watson Multi-Agent Test Harness{RESET}")
    print(f"{BOLD}  Spec: watcher-policy.md{RESET}")
    print(f"{BOLD}{'=' * 66}{RESET}")

    for title, event in scenarios:
        divider(title)
        result = await watson.intercept(event)

        print(f"\n  {BOLD}[JOURNEY RESULT]{RESET}")
        print(f"  Status  : {result['status']}")
        print(f"  Handler : {result['handler']}")
        if "report" in result:
            indented = textwrap.indent(result["report"], "    ")
            print(f"\n{indented}")
        print()

    divider("하네스 실행 완료")
    print(f"  {GREEN}✓ Scenario 1{RESET} : Watson → Holmes (일반 종결)")
    print(f"  {MAGENTA}✓ Scenario 2{RESET} : Watson → StarCraft → Faker (에스컬레이션)")
    print()


if __name__ == "__main__":
    asyncio.run(run_harness())
