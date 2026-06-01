"""음성 감정 분석 — 외부 API 연동 전 플레이스홀더."""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


def analyze_emotion(audio_path: str) -> dict[str, float]:
    """
    추출된 WAV 경로를 받아 감정 점수 dict를 반환합니다.

    현재는 고정 스텁만 반환합니다. 아래 중 하나로 교체하면 됩니다.

    **1) Hume AI (Speech Prosody 등)**
    - https://dev.hume.ai/docs — API 키를 `HUME_API_KEY` 등 환경변수로 두고
    - `requests.post` 로 오디오 파일/바이너리를 보내 응답 JSON을 파싱해
    - `{"sadness": 0.0~1.0, "passion": 0.0~1.0, ...}` 형태로 매핑합니다.

    **2) Hugging Face Inference API (음성 감정 분류 모델)**
    - 예: `superb/wav2vec2-base-superb-er` 등 감정 인식 체크포인트
    - https://huggingface.co/inference-api — 토큰으로 POST, 라벨·score를 emotions에 반영

    **3) 로컬 transformers**
    - GPU/지연 허용 시 파이프라인 로드 후 `audio_path` 로드 추론

    코드 리마인더:
        import requests
        with open(audio_path, "rb") as f:
            r = requests.post(HUME_ENDPOINT, headers={"Authorization": ...}, data=f.read())
        # 응답 스키마에 맞게 정규화
    """
    if not os.path.isfile(audio_path):
        logger.warning("[emotion] 파일 없음: %s", audio_path)
        return _neutral_stub()

    logger.info("[emotion] 플레이스홀더 분석 (외부 API 미연동): %s", audio_path)
    return _neutral_stub()


def _neutral_stub() -> dict[str, float]:
    """기획 예시 포맷 — 실제 연동 시 API가 주는 라벨로 채움."""
    return {
        "sadness": 0.05,
        "passion": 0.12,
        "neutral": 0.83,
    }


def emotions_for_json(em: dict[str, float]) -> dict[str, float]:
    """응답 JSON용 — 값만 float 로 제한."""
    out: dict[str, float] = {}
    for k, v in em.items():
        try:
            out[str(k)] = float(v)
        except (TypeError, ValueError):
            continue
    return out if out else _neutral_stub()
