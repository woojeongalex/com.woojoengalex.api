"""[Layer: Ports] 스피치 입력 Port — 주제·평가 저장 (inbound → usecase)."""

from abc import ABC, abstractmethod

from music.app.dtos.speech_dto import (
    SpeechEvaluationCreateCommand,
    SpeechEvaluationResultDto,
    SpeechTopicsResultDto,
)


class SpeechUseCase(ABC):
    @abstractmethod
    def list_topics(self) -> SpeechTopicsResultDto:
        pass

    @abstractmethod
    async def save_evaluation(
        self, command: SpeechEvaluationCreateCommand
    ) -> SpeechEvaluationResultDto:
        pass
