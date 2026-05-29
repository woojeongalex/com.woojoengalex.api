"""[Layer: Interface Adapters] PG 기반 TitanicUseCaseFactory 구현."""

from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic.adapter.outbound.pg.walter_pg_repository import WalterPgRepository
from titanic.app.factories.titanic_use_case_factory import TitanicUseCaseFactory
from titanic.app.use_cases.james_command import JamesCommandImpl
from titanic.app.use_cases.walter_query import WalterQueryImpl


class PgTitanicUseCaseFactory(TitanicUseCaseFactory):
    db: AsyncSession

    @staticmethod
    def create_james_use_case() -> Type[JamesCommandImpl]:
        JamesPgRepository.db = PgTitanicUseCaseFactory.db
        JamesCommandImpl.repository = JamesPgRepository
        return JamesCommandImpl

    @staticmethod
    def create_walter_use_case() -> Type[WalterQueryImpl]:
        WalterPgRepository.db = PgTitanicUseCaseFactory.db
        WalterQueryImpl.repository = WalterPgRepository
        return WalterQueryImpl
