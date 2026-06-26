from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def handle_hub_errors(exc: Exception) -> None:
    """Hub 레이어 예외 → HTTP 예외 변환."""
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=404, detail=str(exc))
    if isinstance(exc, IntegrityError):
        raise HTTPException(status_code=409, detail="이미 존재하는 도메인 키입니다.")
    raise HTTPException(status_code=500, detail="허브 내부 오류가 발생했습니다.")
