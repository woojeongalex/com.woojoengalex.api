from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTestSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTestResponse


class CalTestUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, schema: CalTestSchema) -> CalTestResponse:
        '''칼 헉클리의 자기소개 메소드'''
        pass
