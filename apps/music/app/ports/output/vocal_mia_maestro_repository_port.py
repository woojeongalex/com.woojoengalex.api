"""[Layer: Ports] 보컬 평가 출력 Port — 3NF 번들 저장 계약."""
from __future__ import annotations

from abc import ABC, abstractmethod

from music.app.dtos.evaluation_dto import VocalEvaluationCreateCommand, VocalEvaluationResultDto


class EvaluationRepositoryPort(ABC):
    @abstractmethod
    async def save_evaluation_bundle(
        self, command: VocalEvaluationCreateCommand
    ) -> VocalEvaluationResultDto:
        pass
