"""Vision inbound — 도메인/검증 예외를 HTTPException으로 매핑."""

from fastapi import HTTPException


def handle_vision_error(exc: Exception) -> HTTPException:
    if isinstance(exc, ValueError):
        return HTTPException(status_code=400, detail=str(exc))
    if isinstance(exc, NotImplementedError):
        return HTTPException(
            status_code=501, detail="vision 모델이 아직 연동되지 않았습니다."
        )
    return HTTPException(status_code=500, detail="vision 처리 중 오류가 발생했습니다.")
