"""[Layer: Ports] 악기 튜닝 입력 Port — 카탈로그·평가 저장 (inbound → usecase)."""

from abc import ABC, abstractmethod

from music.app.dtos.instrument_dto import (
    InstrumentCatalogResultDto,
    InstrumentEvaluationCreateCommand,
    InstrumentEvaluationResultDto,
)


class InstrumentUseCase(ABC):
    @abstractmethod
    def list_catalog(self, q: str = "") -> InstrumentCatalogResultDto:
        pass

    @abstractmethod
    async def save_evaluation(
        self, command: InstrumentEvaluationCreateCommand
    ) -> InstrumentEvaluationResultDto:
        pass
