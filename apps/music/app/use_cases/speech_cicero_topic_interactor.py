from __future__ import annotations

import logging

from music.app.dtos.speech_dto import SpeechTopicHitDto, SpeechTopicsResultDto
from music.app.ports.input.speech_cicero_topic_use_case import SpeechTopicUseCase
from music.domain.speech_cicero_topic_catalog import list_speech_topics

logger = logging.getLogger(__name__)


class CiceroTopicInteractor(SpeechTopicUseCase):
    def read_topics(self) -> SpeechTopicsResultDto:
        hits = [
            SpeechTopicHitDto(
                topic_id=item.topic_id,
                label=item.label,
                description=item.description,
            )
            for item in list_speech_topics()
        ]
        logger.info("[MUSIC][cicero][4/interactor] 주제 조회 count=%d", len(hits))
        return SpeechTopicsResultDto(hits=hits, count=len(hits))
