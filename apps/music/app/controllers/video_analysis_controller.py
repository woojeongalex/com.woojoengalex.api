"""비디오 보컬 분석 HTTP 진입점."""

from __future__ import annotations

import logging

from music.app.schemas.video_analysis_schema import VideoVocalAnalysisResponse
from music.app.services.video_analysis_service import VideoAnalysisService

logger = logging.getLogger(__name__)


class VideoAnalysisController:
    def __init__(self) -> None:
        self._service = VideoAnalysisService()

    def analyze_video_upload(
        self, file_bytes: bytes, original_filename: str
    ) -> VideoVocalAnalysisResponse:
        logger.info(
            "[MUSIC][video_analysis][2/controller] analyze bytes=%s name=%s",
            len(file_bytes),
            original_filename,
        )
        return self._service.analyze_video_bytes(file_bytes, original_filename)
