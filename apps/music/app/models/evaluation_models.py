"""보컬 평가 세션·AI 분석 엔티티 재노출."""

from music.app.models.ai_vocal_analysis_model import AiVocalAnalysisEntity
from music.app.models.sing_model import SingEvaluationEntity
from music.app.models.user_vocal_recording_model import UserVocalRecordingEntity

__all__ = [
    "SingEvaluationEntity",
    "UserVocalRecordingEntity",
    "AiVocalAnalysisEntity",
    "AiVocalAnalysisEvaluationEntity",
]

# 호환 alias (기존 import 경로)
AiVocalAnalysisEvaluationEntity = SingEvaluationEntity
