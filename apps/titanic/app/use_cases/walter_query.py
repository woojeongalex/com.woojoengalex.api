"""[Layer: Use Cases] Walter — read 업무 오케스트레이션."""

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.ports.output.walter_repository_port import WalterRepositoryPort
from titanic.app.titanic_flow_log import titanic_flow_log


class WalterQuery(ABC):
    @abstractmethod
    async def read_passengers(
        source_file: str | None, page: int, page_size: int
    ) -> dict[str, Any]:
        pass


class WalterQueryImpl(WalterQuery, WalterUseCase):
    repository: type[WalterRepositoryPort]

    @staticmethod
    async def read_passengers(
        source_file: str | None, page: int, page_size: int
    ) -> dict[str, Any]:
        titanic_flow_log(
            "walter-read",
            "usecase",
            "read_passengers page=%s size=%s",
            page,
            page_size,
            source_file=source_file or "latest",
        )
        return await WalterQueryImpl.repository.read_passengers(
            source_file, page, page_size
        )
