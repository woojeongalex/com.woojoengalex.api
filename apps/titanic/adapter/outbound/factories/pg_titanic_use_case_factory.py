"""[Layer: Interface Adapters] PG 기반 TitanicUseCaseFactory 구현."""

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.crew_james_pg_repository import JamesPgRepository
from titanic.app.factories.titanic_use_case_factory import TitanicUseCaseFactory
from titanic.app.ports.input.crew_james_use_case import JamesUseCase
from titanic.app.ports.input.crew_walter_use_case import WalterUseCase
from titanic.app.use_cases.crew_james_interactor import JamesInteractor
from titanic.app.use_cases.crew_walter_interactor import WalterInteractor
from titanic.adapter.outbound.pg.crew_walter_pg_repository import WalterPgRepository


class PgTitanicUseCaseFactory(TitanicUseCaseFactory):
    db: AsyncSession

    @staticmethod
    def create_james_use_case() -> JamesUseCase:
        return JamesInteractor(JamesPgRepository(PgTitanicUseCaseFactory.db))

    @staticmethod
    def create_walter_use_case() -> WalterUseCase:
        return WalterInteractor(WalterPgRepository(PgTitanicUseCaseFactory.db))
