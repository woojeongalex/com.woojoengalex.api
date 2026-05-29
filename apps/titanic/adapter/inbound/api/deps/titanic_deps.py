"""FastAPI Depends — Abstract Factory로 command/query 조립."""

from typing import Type

from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.factories.pg_titanic_use_case_factory import PgTitanicUseCaseFactory
from titanic.app.factories.titanic_use_case_factory import TitanicUseCaseFactory
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.use_cases.james_command import JamesCommandImpl
from titanic.app.use_cases.walter_query import WalterQueryImpl


def get_titanic_use_case_factory(
    db: AsyncSession = Depends(get_db),
) -> Type[TitanicUseCaseFactory]:
    PgTitanicUseCaseFactory.db = db
    return PgTitanicUseCaseFactory


def build_james_use_case(db: AsyncSession) -> Type[JamesUseCase]:
    PgTitanicUseCaseFactory.db = db
    return PgTitanicUseCaseFactory.create_james_use_case()


def get_walter_use_case(
    factory: Type[TitanicUseCaseFactory] = Depends(get_titanic_use_case_factory),
) -> Type[WalterUseCase]:
    return factory.create_walter_use_case()
