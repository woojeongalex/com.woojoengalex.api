from __future__ import annotations

import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_cal_tester_dto import CalTestQuery, CalTestResponse
from titanic.app.ports.output.passenger_cal_tester_repository import CalTestRepository

logger = logging.getLogger(__name__)


class CalTestPgRepository(CalTestRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: CalTestQuery) -> CalTestResponse:
        logger.info(f"[CalTestPgRepository] introduce_myself 진입 | request_data={query}")

        response: CalTestResponse = CalTestResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )
        return response