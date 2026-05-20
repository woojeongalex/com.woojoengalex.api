"""3단계 AI 보컬 분석 결과 — Neon `vocal_sing_results` 테이블."""

from music.app.models.sing_model import VocalSingResultEntity

__all__ = ["AiVocalAnalysisResultEntity"]

# UI 순서(음정 → 박자 → 등급·요약)와 동일한 컬럼을 갖는 행. 테이블·매핑은 `sing_model` 단일 정의를 공유한다.
AiVocalAnalysisResultEntity = VocalSingResultEntity
