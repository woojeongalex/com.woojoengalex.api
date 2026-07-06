import asyncio
import logging
import os

import cv2
import numpy as np
from torch import Tensor
from ultralytics import YOLO
from vision.app.dtos.vision_dto import AnalyzeImageCommand, VisionResult
from vision.app.factories.face_classifier_factory import classify_face
from vision.app.ports.input.vision_use_case import VisionUseCase
from vision.app.ports.output.vision_repository_port import VisionRepositoryPort

logger = logging.getLogger(__name__)

_MODEL_PATH = os.getenv("VISION_MODEL_PATH", "yolov8n.pt")
_FACE_MATCH_THRESHOLD = 0.5
_model_cache: YOLO | None = None


def _get_model() -> YOLO:
    global _model_cache
    if _model_cache is None:
        logger.info("[VisionInteractor] 모델 로드: %s", _MODEL_PATH)
        _model_cache = YOLO(_MODEL_PATH)
    return _model_cache


class VisionInteractor(VisionUseCase):
    def __init__(self, repository: VisionRepositoryPort) -> None:
        self.repository = repository

    async def analyze(self, command: AnalyzeImageCommand) -> VisionResult:
        logger.info("[VisionInteractor] analyze | file_name=%s", command.file_name)
        label, confidence = await asyncio.to_thread(
            self._run_model, command.image_bytes
        )
        return await self.repository.save(command.file_name, label, confidence)

    def _run_model(self, image_bytes: bytes) -> tuple[str, float]:
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("이미지를 디코딩할 수 없습니다.")

        model = _get_model()
        results = model(image, verbose=False)
        boxes = results[0].boxes
        if boxes is None or len(boxes) == 0:
            return "인식된 객체 없음", 0.0

        best_idx = int(boxes.conf.argmax())
        label = model.names[int(boxes.cls[best_idx])]
        confidence = float(boxes.conf[best_idx])

        if label == "person":
            identified = self._identify_person(image, boxes.xyxy[best_idx])
            if identified is not None:
                return identified

        return label, confidence

    def _identify_person(
        self, image: np.ndarray, box_xyxy: Tensor
    ) -> tuple[str, float] | None:
        x1, y1, x2, y2 = (int(v) for v in box_xyxy.tolist())
        cropped = image[max(y1, 0) : y2, max(x1, 0) : x2]
        if cropped.size == 0:
            return None

        try:
            face_label, face_confidence = classify_face(cropped)
        except Exception:
            logger.exception("[VisionInteractor] 얼굴 식별 실패 — person으로 폴백")
            return None

        if face_confidence < _FACE_MATCH_THRESHOLD:
            return None
        return face_label, face_confidence

    async def list_results(self) -> list[VisionResult]:
        logger.info("[VisionInteractor] list_results")
        return await self.repository.find_all()
