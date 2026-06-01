"""[Layer: Interface Adapters] PG 기반 TitanicUseCaseFactory 구현."""

from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic.adapter.outbound.pg.walter_pg_repository import WalterPgRepository
from titanic.app.factories.titanic_use_case_factory import TitanicUseCaseFactory
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.use_cases.james_interactor import JamesInteractor
from titanic.app.use_cases.walter_interactor import WalterInteractor


class PgTitanicUseCaseFactory(TitanicUseCaseFactory):
    db: AsyncSession

    @staticmethod
    def create_james_use_case() -> Type[JamesUseCase]:
        JamesPgRepository.db = PgTitanicUseCaseFactory.db
        JamesInteractor.repository = JamesPgRepository
        return JamesInteractor

    @staticmethod
    def create_walter_use_case() -> Type[WalterUseCase]:
        WalterPgRepository.db = PgTitanicUseCaseFactory.db
        WalterInteractor.repository = WalterPgRepository
        return WalterInteractor
