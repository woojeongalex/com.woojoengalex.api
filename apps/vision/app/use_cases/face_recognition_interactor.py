import asyncio
import logging

import cv2
import numpy as np
from vision.app.dtos.vision_dto import AnalyzeImageCommand, VisionResult
from vision.app.factories.face_classifier_factory import classify_face
from vision.app.ports.input.vision_use_case import VisionUseCase
from vision.app.ports.output.vision_repository_port import VisionRepositoryPort

logger = logging.getLogger(__name__)


class FaceRecognitionInteractor(VisionUseCase):
    def __init__(self, repository: VisionRepositoryPort) -> None:
        self.repository = repository

    async def analyze(self, command: AnalyzeImageCommand) -> VisionResult:
        logger.info(
            "[FaceRecognitionInteractor] analyze | file_name=%s", command.file_name
        )
        label, confidence = await asyncio.to_thread(
            self._run_model, command.image_bytes
        )
        return await self.repository.save(command.file_name, label, confidence)

    def _run_model(self, image_bytes: bytes) -> tuple[str, float]:
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("이미지를 디코딩할 수 없습니다.")

        return classify_face(image)

    async def list_results(self) -> list[VisionResult]:
        logger.info("[FaceRecognitionInteractor] list_results")
        return await self.repository.find_all()
