"""[Layer: Use Cases] Cicero/Herald 스피치 평가 DTO."""
from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "SpeechEvaluationCreateCommand",
    "SpeechEvaluationResultDto",
    "SpeechTopicHitDto",
    "SpeechTopicsResultDto",
]


@dataclass(frozen=True)
class SpeechTopicHitDto:
    topic_id: str
    label: str
    description: str


@dataclass(frozen=True)
class SpeechTopicsResultDto:
    hits: list[SpeechTopicHitDto]
    count: int


@dataclass(frozen=True)
class SpeechEvaluationCreateCommand:
    topic_id: str
    clarity_score: int
    pace_score: int
    tone_score: int
    summary: str
    feedback_points: list[str]
    file_name: str
    duration_sec: int


@dataclass(frozen=True)
class SpeechEvaluationResultDto:
    id: int
    ok: bool = True
    message: str = "저장되었습니다."
