from __future__ import annotations

import logging

from music.adapter.inbound.api.schemas.speech_herald_recorder_schema import HeraldIntroduceSchema, HeraldIntroduceResponse
from music.app.dtos.speech_dto import HeraldIntroduceQuery, SpeechEvaluationCreateCommand, SpeechEvaluationResultDto
from music.app.ports.input.speech_herald_recorder_use_case import SpeechEvaluationUseCase
from music.app.ports.output.speech_herald_recorder_repository_port import SpeechRepositoryPort
from music.domain.speech_cicero_topic_catalog import get_speech_topic

logger = logging.getLogger(__name__)


class HeraldRecorderInteractor(SpeechEvaluationUseCase):
    def __init__(self, repository: SpeechRepositoryPort) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: HeraldIntroduceSchema) -> HeraldIntroduceResponse:
        return await self.repository.introduce_herald(HeraldIntroduceQuery(id=schema.id, name=schema.name))

    async def upload(
        self, command: SpeechEvaluationCreateCommand
    ) -> SpeechEvaluationResultDto:
        if get_speech_topic(command.topic_id) is None:
            raise ValueError("지원하지 않는 스피치 주제입니다.")
        result = await self.repository.save_evaluation_bundle(command)
        logger.info("[MUSIC][herald][4/interactor] 저장 eval=%s", result.id)
        return result
