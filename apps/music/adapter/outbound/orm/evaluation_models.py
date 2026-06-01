"""보컬 평가 세션·AI 분석 엔티티 재노출."""

from music.adapter.outbound.orm.ai_vocal_analysis_model import AiVocalAnalysisEntity
from music.adapter.outbound.orm.sing_model import SingEvaluationEntity
from music.adapter.outbound.orm.user_vocal_recording_model import UserVocalRecordingEntity

__all__ = [
    "SingEvaluationEntity",
    "UserVocalRecordingEntity",
    "AiVocalAnalysisEntity",
    "AiVocalAnalysisEvaluationEntity",
]

# 호환 alias (기존 import 경로)
AiVocalAnalysisEvaluationEntity = SingEvaluationEntity
