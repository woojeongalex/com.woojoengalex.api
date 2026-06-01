"""Titanic Use Case 조립 — DB 세션은 여기서만 주입."""

from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.factories.pg_titanic_use_case_factory import PgTitanicUseCaseFactory
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.input.walter_use_case import WalterUseCase


def get_james_use_case(db: AsyncSession = Depends(get_db)) -> type[JamesUseCase]:
    PgTitanicUseCaseFactory.db = db
    return PgTitanicUseCaseFactory.create_james_use_case()


def get_walter_use_case(db: AsyncSession = Depends(get_db)) -> type[WalterUseCase]:
    PgTitanicUseCaseFactory.db = db
    return PgTitanicUseCaseFactory.create_walter_use_case()
