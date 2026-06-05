"""[Layer: Ports] 보컬 평가 입력 Port — 저장 (inbound → usecase)."""

from abc import ABC, abstractmethod

from music.app.dtos.evaluation_dto import (
    VocalEvaluationCreateCommand,
    VocalEvaluationResultDto,
)


class EvaluationUseCase(ABC):
    @abstractmethod
    async def upload(
        self, command: VocalEvaluationCreateCommand
    ) -> VocalEvaluationResultDto:
        pass
