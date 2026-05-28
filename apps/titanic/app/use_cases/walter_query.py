from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from fastapi import Depends
from titanic.adapter.inbound.api.schemas.titanic_schema import WalterPassengerPageResponse
from titanic.app.ports.input.walter_query_port import WalterQueryPort
from titanic.app.ports.output.walter_repository import WalterRepository
from titanic.app.titanic_flow_log import titanic_flow_log


class WalterUseCase:
    """Walter 조회 유스케이스."""

    def __init__(self, repository: WalterRepository | None = None) -> None:
        self._repository = repository

    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageResponse:
        if self._repository is None:
            raise RuntimeError("WalterRepository가 설정되지 않았습니다.")
        titanic_flow_log(
            "walter-read",
            "3/usecase",
            "execute source_file=%s page=%s size=%s to=output",
            source_file or "latest",
            page,
            size,
        )
        return await self._repository.read_passengers(source_file, page, size)

    # 이하 메서드는 구 train_use_case 호환용(현재는 deprecated 경로)
    def _disabled(self) -> None:
        raise RuntimeError(
            "프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다."
        )

    def get_sample_row(self):
        self._disabled()

    def get_passenger_count(self) -> int:
        self._disabled()
        return 0

    def get_survived_count(self) -> int:
        self._disabled()
        return 0

    def get_dead_count(self) -> int:
        self._disabled()
        return 0

    def get_full_data(self):
        self._disabled()


def build_walter_use_case(db: AsyncSession) -> WalterUseCase:
    return WalterUseCase(WalterRepository(db))


class WalterQuery:
    """Walter 조회 Query facade."""

    def __init__(self, use_case: WalterUseCase) -> None:
        self._use_case = use_case

    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageResponse:
        titanic_flow_log(
            "walter-read",
            "2/input",
            "accepted source_file=%s page=%s size=%s to=usecase",
            source_file or "latest",
            page,
            size,
        )
        return await self._use_case.read_passengers(source_file, page, size)


def get_walter_query(db: AsyncSession = Depends(get_db)) -> WalterQueryPort:
    return WalterQuery(build_walter_use_case(db))
