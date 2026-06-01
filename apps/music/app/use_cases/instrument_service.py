import logging

from music.app.instrument_catalog import search_instruments
from music.adapter.outbound.orm.instrument_evaluation_model import InstrumentEvaluationEntity
from music.adapter.outbound.orm.instrument_recording_model import InstrumentRecordingEntity
from music.adapter.outbound.orm.instrument_tuning_analysis_model import (
    InstrumentTuningAnalysisEntity,
)
from music.app.dtos.instrument_dto import (
    InstrumentCatalogHitDto,
    InstrumentCatalogResultDto,
    InstrumentEvaluationCreateCommand,
    InstrumentEvaluationResultDto,
)
from music.app.ports.input.instrument_use_case import InstrumentUseCase
from music.app.ports.output.instrument_repository_port import InstrumentRepositoryPort

logger = logging.getLogger(__name__)


class InstrumentService(InstrumentUseCase):
    def __init__(self, repository: InstrumentRepositoryPort) -> None:
        self._repository = repository

    def list_catalog(self, q: str = "") -> InstrumentCatalogResultDto:
        hits = [
            InstrumentCatalogHitDto(
                instrument_id=item.instrument_id,
                label=item.label,
                description=item.description,
                standard_tuning=item.standard_tuning,
            )
            for item in search_instruments(q)
        ]
        return InstrumentCatalogResultDto(query=q.strip(), hits=hits, count=len(hits))

    async def save_evaluation(
        self, command: InstrumentEvaluationCreateCommand
    ) -> InstrumentEvaluationResultDto:
        evaluation = InstrumentEvaluationEntity(user_id=None)
        recording = InstrumentRecordingEntity(
            instrument_evaluation_id=0,
            user_id=None,
            instrument_id=command.instrument_id,
            file_name=command.file_name or f"{command.instrument_id}-recording",
            duration_sec=command.duration_sec,
        )
        analysis = InstrumentTuningAnalysisEntity(
            instrument_recording_id=0,
            analysis_engine="client_demo",
            tuning_accuracy=command.tuning_accuracy,
            pitch_deviation_cents=command.pitch_deviation_cents,
            summary=command.summary,
            string_readings=command.string_readings,
        )
        saved_eval, _, _ = await self._repository.save_evaluation_bundle(
            evaluation,
            recording,
            analysis,
        )
        logger.info("[MUSIC][instrument][service] 저장 eval=%s", saved_eval.id)
        return InstrumentEvaluationResultDto(id=saved_eval.id)
