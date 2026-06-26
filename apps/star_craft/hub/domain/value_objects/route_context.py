from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RouteContext:
    """허브가 스포크로 라우팅할 때 전달하는 컨텍스트 VO.

    frozen=True: 라우팅 결정 후 변경 불가 (불변 보장)
    """

    domain_key: str          # 라우팅 대상 스포크 식별자
    intent: str              # 사용자 의도 (예: "upload", "search", "analyze")
    payload: dict[str, Any]  # 스포크에 전달할 데이터 (DTO로 변환 후 전달)
    request_id: str          # 요청 추적 ID
    caller_id: str | None = None  # 요청 발신 주체 (사용자 ID 등)

    def is_valid(self) -> bool:
        return bool(self.domain_key and self.intent and self.request_id)
