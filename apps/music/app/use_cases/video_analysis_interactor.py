"""비디오 업로드 → WAV 추출 → librosa + 감정(플레이스홀더) 파이프라인."""

from __future__ import annotations

import logging
import os
import tempfile
import uuid
from pathlib import Path

from music.app.dtos.video_analysis_dto import VideoVocalAnalysisResultDto
from music.app.ports.input.video_analysis_use_case import VideoAnalysisUseCase
from music.app.use_cases.emotion_analysis import analyze_emotion, emotions_for_json
from music.app.use_cases.librosa_vocal_analysis import analyze_pitch_bpm_duration
from music.app.use_cases.video_audio_preprocess import (
    VIDEO_EXTENSIONS,
    extract_audio_wav_from_video,
    is_supported_video_filename,
)

logger = logging.getLogger(__name__)


class VideoAnalysisInteractor(VideoAnalysisUseCase):
    """상태 없음 — 바이트 단위 분석."""

    def analyze(
        self, data: bytes, original_filename: str
    ) -> VideoVocalAnalysisResultDto:
        if not data:
            raise ValueError("업로드 파일이 비어 있습니다.")
        name = original_filename or "video.bin"
        if not is_supported_video_filename(name):
            allowed = ", ".join(sorted(VIDEO_EXTENSIONS))
            raise ValueError(f"지원하지 않는 확장자입니다. 허용: {allowed}")

        suffix = Path(name).suffix.lower() or ".mp4"

        with tempfile.TemporaryDirectory(prefix="vocal_vid_") as tmp:
            vid_path = os.path.join(tmp, f"in_{uuid.uuid4().hex}{suffix}")
            wav_path = os.path.join(tmp, "extracted.wav")

            with open(vid_path, "wb") as f:
                f.write(data)

            extract_audio_wav_from_video(vid_path, wav_path)

            lib_out = analyze_pitch_bpm_duration(wav_path)
            raw_emotion = analyze_emotion(wav_path)
            emotions = emotions_for_json(raw_emotion)

        return VideoVocalAnalysisResultDto(
            pitch_data=lib_out["pitch_data"],
            bpm=lib_out["bpm"],
            duration=lib_out["duration"],
            emotions=emotions,
        )
