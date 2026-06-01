"""비디오 파일 → WAV 추출 (moviepy). 시스템에 ffmpeg가 있어야 하는 환경이 많습니다."""

from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# 지원 확장자 (소문자 기준)
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v"}


def is_supported_video_filename(name: str) -> bool:
    return Path(name).suffix.lower() in VIDEO_EXTENSIONS


def extract_audio_wav_from_video(video_path: str, wav_out_path: str, sr: int = 22050) -> None:
    """
    moviepy로 비디오에서 오디오를 떼어 PCM WAV로 저장합니다.

    :param video_path: 원본 비디오 경로
    :param wav_out_path: 출력 WAV 경로 (.wav)
    :param sr: 샘플레이트 (librosa 분석과 맞춤)
    """
    try:
        from moviepy import VideoFileClip
    except ImportError:
        from moviepy.editor import VideoFileClip  # type: ignore[no-redef]

    clip = VideoFileClip(video_path)
    try:
        if clip.audio is None:
            raise ValueError("비디오에 오디오 트랙이 없습니다.")
        # WAV(PCM): librosa.load 에 바로 넘기기 좋음
        clip.audio.write_audiofile(
            wav_out_path,
            fps=sr,
            nbytes=2,
            codec="pcm_s16le",
            logger=None,
        )
    finally:
        clip.close()

    if not os.path.isfile(wav_out_path) or os.path.getsize(wav_out_path) == 0:
        raise RuntimeError("오디오 추출 결과 WAV 파일이 비어 있거나 생성되지 않았습니다.")

    logger.info(
        "[video_preprocess] WAV 추출 완료 sr=%s out=%s",
        sr,
        wav_out_path,
    )
