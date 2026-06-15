"""Instrument(Franz/Andrew) 의존성 조립소 — 카탈로그 검색·평가 업로드."""
from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from music.adapter.outbound.pg.instrument_andrew_recorder_pg_repository import AndrewRecorderPgRepository
from music.app.ports.input.instrument_andrew_recorder_use_case import InstrumentEvaluationUseCase
from music.app.ports.input.instrument_franz_catalog_use_case import InstrumentCatalogUseCase
from music.app.ports.output.instrument_andrew_recorder_repository_port import InstrumentRepositoryPort
from music.app.use_cases.instrument_andrew_recorder_interactor import AndrewRecorderInteractor


def get_instrument_repository(db: AsyncSession = Depends(get_db)) -> InstrumentRepositoryPort:
    return AndrewRecorderPgRepository(session=db)


def get_instrument_catalog_use_case(
    repository: InstrumentRepositoryPort = Depends(get_instrument_repository),
) -> InstrumentCatalogUseCase:
    return AndrewRecorderInteractor(repository=repository)


def get_instrument_recorder_use_case(
    repository: InstrumentRepositoryPort = Depends(get_instrument_repository),
) -> InstrumentEvaluationUseCase:
    return AndrewRecorderInteractor(repository=repository)
