"""Instrument 의존성 조립소 — 카탈로그 검색·평가 업로드."""

from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.pg.instrument_pg_repository import InstrumentPgRepository
from music.app.ports.input.instrument_use_case import InstrumentUseCase
from music.app.ports.output.instrument_repository_port import InstrumentRepositoryPort
from music.app.use_cases.instrument_interactor import InstrumentInteractor


def get_instrument_use_case(db: AsyncSession = Depends(get_db)) -> InstrumentUseCase:
    repository: InstrumentRepositoryPort = InstrumentPgRepository(session=db)
    return InstrumentInteractor(repository=repository)
