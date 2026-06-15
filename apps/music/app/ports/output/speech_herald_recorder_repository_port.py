"""[Layer: Ports] 스피치 평가 출력 Port — 3NF 번들 저장 계약."""
from __future__ import annotations

from abc import ABC, abstractmethod

from music.app.dtos.speech_dto import SpeechEvaluationCreateCommand, SpeechEvaluationResultDto


class SpeechRepositoryPort(ABC):
    @abstractmethod
    async def save_evaluation_bundle(
        self, command: SpeechEvaluationCreateCommand
    ) -> SpeechEvaluationResultDto:
        pass
