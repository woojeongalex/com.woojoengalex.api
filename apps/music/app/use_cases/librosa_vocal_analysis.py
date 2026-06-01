"""librosa 기반 음정·템포(BPM)·길이 분석."""

from __future__ import annotations

import logging
from typing import Any

import librosa
import numpy as np

logger = logging.getLogger(__name__)


def analyze_pitch_bpm_duration(wav_path: str, sr: int = 22050) -> dict[str, Any]:
    """
    WAV 파일에 대해 pitch 요약, BPM, duration(초)을 계산합니다.

    - pitch: `librosa.yin` 기반 f0 트랙 요약 + 다운샘플된 contour (JSON 크기 제한)
    - bpm: onset + beat_track
    """
    y, sr = librosa.load(wav_path, sr=sr, mono=True)
    duration = float(librosa.get_duration(y=y, sr=sr))

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo_arr, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    bpm = float(np.atleast_1d(tempo_arr).reshape(-1)[0])

    f0 = librosa.yin(
        y,
        fmin=librosa.note_to_hz("E2"),
        fmax=librosa.note_to_hz("C7"),
        sr=sr,
    )
    # yin 은 종종 음성 없을 때 비현실 값 → 유효 음역대로 마스크
    valid = (f0 > 65.0) & (f0 < 1500.0)
    f0_v = f0[valid]
    mean_hz = float(np.nanmean(f0)) if f0.size else 0.0
    median_hz = float(np.median(f0_v)) if f0_v.size else 0.0

    max_samples = 100
    step = max(1, len(f0) // max_samples)
    f0_sample = [round(float(x), 2) for x in f0[::step][:max_samples]]

    pitch_data: dict[str, Any] = {
        "sample_rate": sr,
        "mean_f0_hz": round(mean_hz, 2),
        "median_f0_hz": round(median_hz, 2),
        "f0_contour_sample": f0_sample,
    }

    logger.info(
        "[librosa_vocal] duration=%.2fs bpm=%.1f mean_f0=%.1f",
        duration,
        bpm,
        mean_hz,
    )

    return {
        "pitch_data": pitch_data,
        "bpm": round(bpm, 2),
        "duration": round(duration, 3),
    }
