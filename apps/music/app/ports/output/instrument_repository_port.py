"""[Layer: Ports] 악기 평가 출력 Port — 3NF 번들 저장 계약."""

from abc import ABC, abstractmethod

from music.adapter.outbound.orm.instrument_evaluation_model import InstrumentEvaluationEntity
from music.adapter.outbound.orm.instrument_recording_model import InstrumentRecordingEntity
from music.adapter.outbound.orm.instrument_tuning_analysis_model import (
    InstrumentTuningAnalysisEntity,
)


class InstrumentRepositoryPort(ABC):
    @abstractmethod
    async def save_evaluation_bundle(
        self,
        evaluation: InstrumentEvaluationEntity,
        recording: InstrumentRecordingEntity,
        analysis: InstrumentTuningAnalysisEntity,
    ) -> tuple[
        InstrumentEvaluationEntity,
        InstrumentRecordingEntity,
        InstrumentTuningAnalysisEntity,
    ]:
        pass
