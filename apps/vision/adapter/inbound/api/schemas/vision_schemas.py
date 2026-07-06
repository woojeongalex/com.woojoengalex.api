from datetime import datetime

from pydantic import BaseModel


class VisionAnalyzeResponse(BaseModel):
    id: int
    file_name: str
    label: str
    confidence: float
    analyzed_at: datetime


class VisionResultListResponse(BaseModel):
    results: list[VisionAnalyzeResponse]
