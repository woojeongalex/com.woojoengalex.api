import asyncio
import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from music.adapter.inbound.api.mappers.music_inbound_mapper import to_video_analysis_response
from music.adapter.inbound.api.schemas.video_analysis_schema import VideoVocalAnalysisResponse
from music.app.ports.input.video_analysis_use_case import VideoAnalysisUseCase
from music.app.use_cases.video_analysis_service import VideoAnalysisService

logger = logging.getLogger(__name__)
video_router = APIRouter(tags=["music-video"])


def _use_case() -> VideoAnalysisUseCase:
    return VideoAnalysisService()


@video_router.post("/api/music/analyze-video", response_model=VideoVocalAnalysisResponse)
async def analyze_video_upload(
    file: UploadFile = File(..., description="노래 부르는 영상 (mp4, mov 등)"),
) -> VideoVocalAnalysisResponse:
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="파일이 비어 있습니다.")
    filename = file.filename or "upload.mp4"
    logger.info(
        "[MUSIC][video_analysis][1/router] POST /api/music/analyze-video file=%s bytes=%s",
        filename,
        len(data),
    )
    try:
        dto = await asyncio.to_thread(
            _use_case().analyze_video_bytes,
            data,
            filename,
        )
        return to_video_analysis_response(dto)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("[MUSIC][video_analysis][1/router] 분석 실패: %s", exc)
        raise HTTPException(
            status_code=502,
            detail="비디오 분석에 실패했습니다. ffmpeg 설치·파일 형식을 확인하거나 로그를 확인하세요.",
        ) from exc
