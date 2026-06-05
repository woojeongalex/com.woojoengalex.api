"""Video(James) 의존성 조립소 — 영상 업로드 분석 (DB 없음)."""

from music.app.ports.input.video_analysis_use_case import VideoAnalysisUseCase
from music.app.use_cases.video_analysis_interactor import VideoAnalysisInteractor


def get_video_use_case() -> VideoAnalysisUseCase:
    return VideoAnalysisInteractor()
