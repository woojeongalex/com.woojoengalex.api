import asyncio
import logging

from fastapi import HTTPException

from music.app.dtos.video_analysis_dto import VideoVocalAnalysisResultDto
from music.app.ports.input.video_analysis_use_case import VideoAnalysisUseCase

logger = logging.getLogger(__name__)


async def pass_video_analysis(
    video: VideoAnalysisUseCase,
    data: bytes,
    filename: str,
) -> VideoVocalAnalysisResultDto:
    try:
        return await asyncio.to_thread(video.analyze, data, filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("[MUSIC][video][handler] 분석 실패: %s", exc)
        raise HTTPException(
            status_code=502,
            detail="비디오 분석에 실패했습니다. ffmpeg 설치·파일 형식을 확인하거나 로그를 확인하세요.",
        ) from exc
