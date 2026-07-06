import logging

from fastapi import APIRouter, Depends, File, UploadFile
from vision.adapter.inbound.api.deps.vision_deps import (
    get_face_recognition_use_case,
    get_vision_use_case,
)
from vision.adapter.inbound.api.handlers.vision_inbound_handlers import (
    handle_vision_error,
)
from vision.adapter.inbound.api.mappers.vision_mapper import result_to_response
from vision.adapter.inbound.api.parsers.vision_upload_parser import (
    read_vision_upload,
)
from vision.adapter.inbound.api.schemas.vision_schemas import (
    VisionAnalyzeResponse,
    VisionResultListResponse,
)
from vision.app.dtos.vision_dto import AnalyzeImageCommand
from vision.app.ports.input.vision_use_case import VisionUseCase

logger = logging.getLogger(__name__)

vision_router = APIRouter(prefix="/api/vision", tags=["vision"])


@vision_router.post("/analyze", response_model=VisionAnalyzeResponse)
async def analyze_image(
    file: UploadFile = File(...),
    vision: VisionUseCase = Depends(get_vision_use_case),
) -> VisionAnalyzeResponse:
    file_name, data = await read_vision_upload(file)
    try:
        result = await vision.analyze(
            AnalyzeImageCommand(file_name=file_name, image_bytes=data)
        )
    except Exception as exc:
        raise handle_vision_error(exc) from exc
    return result_to_response(result)


@vision_router.post("/analyze-face", response_model=VisionAnalyzeResponse)
async def analyze_face(
    file: UploadFile = File(...),
    vision: VisionUseCase = Depends(get_face_recognition_use_case),
) -> VisionAnalyzeResponse:
    file_name, data = await read_vision_upload(file)
    try:
        result = await vision.analyze(
            AnalyzeImageCommand(file_name=file_name, image_bytes=data)
        )
    except Exception as exc:
        raise handle_vision_error(exc) from exc
    return result_to_response(result)


@vision_router.get("/results", response_model=VisionResultListResponse)
async def read_vision_results(
    vision: VisionUseCase = Depends(get_vision_use_case),
) -> VisionResultListResponse:
    results = await vision.list_results()
    return VisionResultListResponse(results=[result_to_response(r) for r in results])
