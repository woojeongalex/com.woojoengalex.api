"""[Layer: Use Cases] Franz/Andrew 악기 평가 DTO."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

__all__ = [
    "InstrumentCatalogHitDto",
    "InstrumentCatalogResultDto",
    "InstrumentEvaluationCreateCommand",
    "InstrumentEvaluationResultDto",
]


@dataclass(frozen=True)
class InstrumentCatalogHitDto:
    instrument_id: str
    label: str
    description: str
    standard_tuning: str


@dataclass(frozen=True)
class InstrumentCatalogResultDto:
    query: str
    hits: list[InstrumentCatalogHitDto]
    count: int


@dataclass(frozen=True)
class InstrumentEvaluationCreateCommand:
    instrument_id: str
    tuning_accuracy: int
    pitch_deviation_cents: int
    summary: str
    string_readings: list[dict[str, Any]]
    file_name: str
    duration_sec: int


@dataclass(frozen=True)
class InstrumentEvaluationResultDto:
    id: int
    ok: bool = True
    message: str = "저장되었습니다."
