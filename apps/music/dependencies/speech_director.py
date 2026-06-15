"""Speech(Cicero/Herald) 의존성 조립소 — 주제 조회·평가 업로드."""
from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.pg.speech_herald_recorder_pg_repository import HeraldRecorderPgRepository
from music.app.ports.input.speech_cicero_topic_use_case import SpeechTopicUseCase
from music.app.ports.input.speech_herald_recorder_use_case import SpeechEvaluationUseCase
from music.app.ports.output.speech_herald_recorder_repository_port import SpeechRepositoryPort
from music.app.use_cases.speech_herald_recorder_interactor import HeraldRecorderInteractor


def get_speech_repository(db: AsyncSession = Depends(get_db)) -> SpeechRepositoryPort:
    return HeraldRecorderPgRepository(session=db)


def get_speech_topic_use_case(
    repository: SpeechRepositoryPort = Depends(get_speech_repository),
) -> SpeechTopicUseCase:
    return HeraldRecorderInteractor(repository=repository)


def get_speech_recorder_use_case(
    repository: SpeechRepositoryPort = Depends(get_speech_repository),
) -> SpeechEvaluationUseCase:
    return HeraldRecorderInteractor(repository=repository)
