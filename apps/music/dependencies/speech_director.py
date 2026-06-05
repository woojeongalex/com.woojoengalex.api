"""Speech 의존성 조립소 — 주제 조회·평가 업로드."""

from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.pg.speech_pg_repository import SpeechPgRepository
from music.app.ports.input.speech_use_case import SpeechUseCase
from music.app.ports.output.speech_repository_port import SpeechRepositoryPort
from music.app.use_cases.speech_interactor import SpeechInteractor


def get_speech_use_case(db: AsyncSession = Depends(get_db)) -> SpeechUseCase:
    repository: SpeechRepositoryPort = SpeechPgRepository(session=db)
    return SpeechInteractor(repository=repository)
