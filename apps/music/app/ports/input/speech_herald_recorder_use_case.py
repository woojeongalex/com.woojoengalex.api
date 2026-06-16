"""[Layer: Ports] 스피치 평가 입력 Port — 평가 저장 (inbound → usecase)."""
from __future__ import annotations

from abc import ABC, abstractmethod

from music.adapter.inbound.api.schemas.speech_herald_recorder_schema import HeraldIntroduceSchema, HeraldIntroduceResponse
from music.app.dtos.speech_dto import (
    SpeechEvaluationCreateCommand,
    SpeechEvaluationResultDto,
)


class SpeechEvaluationUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: HeraldIntroduceSchema) -> HeraldIntroduceResponse:
        pass

    @abstractmethod
    async def upload(
        self, command: SpeechEvaluationCreateCommand
    ) -> SpeechEvaluationResultDto:
        pass
