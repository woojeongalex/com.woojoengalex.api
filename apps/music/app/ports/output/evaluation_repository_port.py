"""[Layer: Ports] 보컬 평가 출력 Port — 3NF 번들 저장 계약."""

from abc import ABC, abstractmethod

from music.adapter.outbound.orm.ai_vocal_analysis_model import AiVocalAnalysisEntity
from music.adapter.outbound.orm.evaluation_models import SingEvaluationEntity
from music.adapter.outbound.orm.user_vocal_recording_model import UserVocalRecordingEntity


class EvaluationRepositoryPort(ABC):
    @abstractmethod
    async def save_evaluation_bundle(
        self,
        evaluation: SingEvaluationEntity,
        vocal_recording: UserVocalRecordingEntity,
        ai_analysis: AiVocalAnalysisEntity,
    ) -> tuple[SingEvaluationEntity, UserVocalRecordingEntity, AiVocalAnalysisEntity]:
        pass
