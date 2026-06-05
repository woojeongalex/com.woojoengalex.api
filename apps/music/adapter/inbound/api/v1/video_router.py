from fastapi import APIRouter, Depends, File, UploadFile

from music.adapter.inbound.api.deps.music_deps import get_video_use_case
from music.adapter.inbound.api.handlers.video_inbound_handlers import pass_video_analysis
from music.adapter.inbound.api.mappers.music_inbound_mapper import to_video_analysis_response
from music.adapter.inbound.api.parsers.video_upload_parser import read_video_upload
from music.adapter.inbound.api.schemas.video_analysis_schema import VideoVocalAnalysisResponse
from music.app.ports.input.video_analysis_use_case import VideoAnalysisUseCase

video_router = APIRouter(tags=["music-video"])


@video_router.post("/api/music/analyze-video", response_model=VideoVocalAnalysisResponse)
async def analyze_video_upload(
    file: UploadFile = File(..., description="노래 부르는 영상 (mp4, mov 등)"),
    video: VideoAnalysisUseCase = Depends(get_video_use_case),
) -> VideoVocalAnalysisResponse:
    filename, data = await read_video_upload(file)
    dto = await pass_video_analysis(video, data, filename)
    return to_video_analysis_response(dto)
