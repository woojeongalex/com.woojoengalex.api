from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AnalyzeImageCommand:
    file_name: str
    image_bytes: bytes


@dataclass(frozen=True)
class VisionResult:
    id: int
    file_name: str
    label: str
    confidence: float
    analyzed_at: datetime
