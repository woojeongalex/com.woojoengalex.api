from __future__ import annotations

import logging

from music.app.dtos.instrument_dto import InstrumentEvaluationCreateCommand, InstrumentEvaluationResultDto
from music.app.ports.input.instrument_andrew_recorder_use_case import InstrumentEvaluationUseCase
from music.app.ports.output.instrument_andrew_recorder_repository_port import InstrumentRepositoryPort

logger = logging.getLogger(__name__)


class AndrewRecorderInteractor(InstrumentEvaluationUseCase):
    def __init__(self, repository: InstrumentRepositoryPort) -> None:
        self.repository = repository

    async def upload(
        self, command: InstrumentEvaluationCreateCommand
    ) -> InstrumentEvaluationResultDto:
        result = await self.repository.save_evaluation_bundle(command)
        logger.info("[MUSIC][andrew][4/interactor] 저장 eval=%s", result.id)
        return result
