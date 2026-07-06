from vision.adapter.inbound.api.schemas.vision_schemas import VisionAnalyzeResponse
from vision.app.dtos.vision_dto import VisionResult


def result_to_response(r: VisionResult) -> VisionAnalyzeResponse:
    return VisionAnalyzeResponse(
        id=r.id,
        file_name=r.file_name,
        label=r.label,
        confidence=r.confidence,
        analyzed_at=r.analyzed_at,
    )
