"""[Layer: Ports] 악기 평가 입력 Port — 평가 저장 (inbound → usecase)."""
from __future__ import annotations

from abc import ABC, abstractmethod

from music.app.dtos.instrument_dto import (
    InstrumentEvaluationCreateCommand,
    InstrumentEvaluationResultDto,
)


class InstrumentEvaluationUseCase(ABC):
    @abstractmethod
    async def upload(
        self, command: InstrumentEvaluationCreateCommand
    ) -> InstrumentEvaluationResultDto:
        pass
