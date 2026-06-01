"""보컬 평가 API 타입 — `evaluation_schemas` 정본을 재노출."""

from music.adapter.inbound.api.schemas.evaluation_schemas import (
    VocalEvaluationCreateRequest as SingEvaluationCreateRequest,
    VocalEvaluationResponse as SingEvaluationResponse,
)

__all__ = ["SingEvaluationCreateRequest", "SingEvaluationResponse"]
