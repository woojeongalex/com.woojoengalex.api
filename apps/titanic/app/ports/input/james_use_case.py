from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.titanic_request import TitanicCommandRequest
from titanic.app.ports.output.james_repository import JamesRepository
from titanic.app.titanic_flow_log import titanic_flow_log


class JamesUseCase:
    """CSV 업로드 command rows → 출력 포트(Repository)로 전달."""

    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def receive_uploaded_rows(
        self,
        file_name: str,
        rows: list[TitanicCommandRequest],
    ) -> dict[str, object]:
        titanic_flow_log(
            "james-upload",
            "2/input",
            "accepted file=%s rows=%s",
            file_name,
            len(rows),
        )
        titanic_flow_log(
            "james-upload",
            "3/usecase",
            "execute file=%s rows=%s to=output",
            file_name,
            len(rows),
        )
        return await self._repository.move_uploaded_rows(file_name, rows)


def build_james_use_case(db: AsyncSession) -> JamesUseCase:
    return JamesUseCase(JamesRepository(db))
