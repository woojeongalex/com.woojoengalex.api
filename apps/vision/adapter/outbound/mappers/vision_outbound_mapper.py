from vision.adapter.outbound.orm.vision_model import VisionModel
from vision.app.dtos.vision_dto import VisionResult


def result_to_model(file_name: str, label: str, confidence: float) -> VisionModel:
    return VisionModel(file_name=file_name, label=label, confidence=confidence)


def model_to_result(model: VisionModel) -> VisionResult:
    return VisionResult(
        id=model.id,
        file_name=model.file_name,
        label=model.label,
        confidence=model.confidence,
        analyzed_at=model.analyzed_at,
    )
