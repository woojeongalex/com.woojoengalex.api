import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.instrument_catalog import search_instruments
from music.app.models.instrument_evaluation_model import InstrumentEvaluationEntity
from music.app.models.instrument_recording_model import InstrumentRecordingEntity
from music.app.models.instrument_tuning_analysis_model import InstrumentTuningAnalysisEntity
from music.app.repositories.bundle_repository import save_three_part_bundle
from music.app.schemas.instrument_schemas import (
    InstrumentCatalogHit,
    InstrumentCatalogResponse,
    InstrumentEvaluationCreateRequest,
    InstrumentEvaluationResponse,
)

logger = logging.getLogger(__name__)


class InstrumentService:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self._db = db

    def _require_db(self) -> AsyncSession:
        if self._db is None:
            raise RuntimeError("DB session is not available.")
        return self._db

    def list_catalog(self, q: str = "") -> InstrumentCatalogResponse:
        hits = [
            InstrumentCatalogHit(
                instrument_id=item.instrument_id,
                label=item.label,
                description=item.description,
                standard_tuning=item.standard_tuning,
            )
            for item in search_instruments(q)
        ]
        return InstrumentCatalogResponse(query=q.strip(), hits=hits, count=len(hits))

    async def save_evaluation(
        self, body: InstrumentEvaluationCreateRequest
    ) -> InstrumentEvaluationResponse:
        evaluation = InstrumentEvaluationEntity(user_id=None)
        recording = InstrumentRecordingEntity(
            instrument_evaluation_id=0,
            user_id=None,
            instrument_id=body.instrument_id,
            file_name=body.file_name or f"{body.instrument_id}-recording",
            duration_sec=body.duration_sec,
        )
        analysis = InstrumentTuningAnalysisEntity(
            instrument_recording_id=0,
            analysis_engine="client_demo",
            tuning_accuracy=body.tuning_accuracy,
            pitch_deviation_cents=body.pitch_deviation_cents,
            summary=body.summary,
            string_readings=body.string_readings,
        )
        saved_eval, _, _ = await save_three_part_bundle(
            self._require_db(),
            evaluation,
            recording,
            analysis,
            recording_fk_attr="instrument_evaluation_id",
            analysis_fk_attr="instrument_recording_id",
            log_label="instrument",
        )
        logger.info("[MUSIC][instrument][service] 저장 eval=%s", saved_eval.id)
        return InstrumentEvaluationResponse(id=saved_eval.id)
