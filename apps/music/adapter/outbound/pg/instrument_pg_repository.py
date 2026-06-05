from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.orm.instrument_evaluation_model import InstrumentEvaluationEntity
from music.adapter.outbound.orm.instrument_recording_model import InstrumentRecordingEntity
from music.adapter.outbound.orm.instrument_tuning_analysis_model import (
    InstrumentTuningAnalysisEntity,
)
from music.adapter.outbound.pg.pg_bundle_repository import save_three_part_bundle
from music.app.ports.output.instrument_repository_port import InstrumentRepositoryPort


class InstrumentPgRepository(InstrumentRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

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
        return await save_three_part_bundle(
            self._session,
            evaluation,
            recording,
            analysis,
            recording_fk_attr="instrument_evaluation_id",
            analysis_fk_attr="instrument_recording_id",
            log_label="instrument",
        )
