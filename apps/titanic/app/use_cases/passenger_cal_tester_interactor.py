from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTestSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTestQuery, CalTestResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTestUseCase
from titanic.app.ports.output.passenger_cal_tester_repository import CalTestRepository


class CalTestInteractor(CalTestUseCase):
    def __init__(self, repository: CalTestRepository):
        self.repository = repository

    async def introduce_myself(self, schema: CalTestSchema) -> CalTestResponse:
        '''칼 헉클리의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(CalTestQuery(
            id=schema.id,
            name=schema.name
        ))
