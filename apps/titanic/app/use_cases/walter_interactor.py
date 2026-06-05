"""[Layer: Use Cases] Walter — 승객 조회."""

import logging

from titanic.app.dtos.walter_page import WalterPassengerPageDto
from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.ports.output.walter_repository_port import WalterRepositoryPort

logger = logging.getLogger(__name__)


class WalterInteractor(WalterUseCase):
    def __init__(self, repository: WalterRepositoryPort) -> None:
        self._repository = repository

    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageDto:
        result = await self._repository.read_passengers(source_file, page, size)
        logger.info("###############################################")
        logger.info("💊[월터 유스케이스] 레포지터리 조회 결과")
        logger.info(f"👍🏻total: {result.total}")
        logger.info(f"🐥page: {result.page}")
        logger.info(f"🦜상위 5개: {result.rows[:5]}")
        logger.info("###############################################")
        return result
