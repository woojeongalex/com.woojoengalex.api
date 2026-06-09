from database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.crew_walter_pg_repository import WalterPgRepository
from titanic.app.ports.input.crew_walter_use_case import WalterUseCase
from titanic.app.ports.output.crew_walter_director_repository import WalterDirectorRepository
from titanic.app.use_cases.crew_walter_interactor import WalterInteractor


def get_walter_use_case(db: AsyncSession = Depends(get_db)) -> WalterUseCase:
    repository: WalterDirectorRepository = WalterPgRepository(session=db)
    return WalterInteractor(repository=repository)
