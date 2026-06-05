"""[Layer: Ports] 비디오 보컬 분석 입력 Port — 바이트 분석 (inbound → usecase)."""

from abc import ABC, abstractmethod

from music.app.dtos.video_analysis_dto import VideoVocalAnalysisResultDto


class VideoAnalysisUseCase(ABC):
    @abstractmethod
    def analyze(
        self, data: bytes, original_filename: str
    ) -> VideoVocalAnalysisResultDto:
        pass
