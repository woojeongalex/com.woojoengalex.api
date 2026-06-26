from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RouteCommand:
    """라우팅 요청 Command DTO (inbound → UseCase)."""

    domain_key: str
    intent: str
    payload: dict[str, Any]
    request_id: str
    caller_id: str | None = None


@dataclass(frozen=True)
class RouteResult:
    """라우팅 처리 결과 DTO (UseCase → inbound)."""

    routed_to: str          # 실제 라우팅된 스포크 domain_key
    result: dict[str, Any]
    request_id: str
    success: bool = True
    error_message: str | None = None
