"""[Layer: Ports] 스피치 평가 출력 Port — 3NF 번들 저장 계약."""

from abc import ABC, abstractmethod

from music.adapter.outbound.orm.speech_evaluation_model import SpeechEvaluationEntity
from music.adapter.outbound.orm.speech_feedback_analysis_model import (
    SpeechFeedbackAnalysisEntity,
)
from music.adapter.outbound.orm.speech_recording_model import SpeechRecordingEntity


class SpeechRepositoryPort(ABC):
    @abstractmethod
    async def save_evaluation_bundle(
        self,
        evaluation: SpeechEvaluationEntity,
        recording: SpeechRecordingEntity,
        analysis: SpeechFeedbackAnalysisEntity,
    ) -> tuple[SpeechEvaluationEntity, SpeechRecordingEntity, SpeechFeedbackAnalysisEntity]:
        pass
