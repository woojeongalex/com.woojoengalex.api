from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VideoVocalAnalysisResultDto:
    pitch_data: dict[str, Any]
    bpm: float
    duration: float
    emotions: dict[str, float]
