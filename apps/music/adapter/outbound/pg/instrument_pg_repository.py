from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.orm.instrument_evaluation_model import InstrumentEvaluationEntity
from music.adapter.outbound.orm.instrument_recording_model import InstrumentRecordingEntity
from music.adapter.outbound.orm.instrument_tuning_analysis_model import (
    InstrumentTuningAnalysisEntity,
)
from music.adapter.outbound.pg.pg_bundle_repository import save_three_part_bundle
from music.app.ports.output.instrument_repository_port import InstrumentRepositoryPort


class InstrumentRepository(InstrumentRepositoryPort):
    def __init__(self, db: AsyncSession | None = None) -> None:
        self._db = db

    def _require_db(self) -> AsyncSession:
        if self._db is None:
            raise RuntimeError("DB session is not available.")
        return self._db

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
            self._require_db(),
            evaluation,
            recording,
            analysis,
            recording_fk_attr="instrument_evaluation_id",
            analysis_fk_attr="instrument_recording_id",
            log_label="instrument",
        )
