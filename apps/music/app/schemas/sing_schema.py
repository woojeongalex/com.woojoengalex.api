"""보컬 결과 API 타입 — `result_schemas` 정본(AI 분석 3단계 필드 순)을 재노출."""

from music.app.schemas.result_schemas import (
    AiVocalAnalysisResultCreateRequest as SingResultCreateRequest,
    AiVocalAnalysisResultResponse as SingResultResponse,
)

__all__ = ["SingResultCreateRequest", "SingResultResponse"]
