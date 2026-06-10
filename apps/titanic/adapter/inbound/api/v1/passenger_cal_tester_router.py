from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTestSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTestResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTestUseCase
from titanic.dependencies.passenger_cal_tester_provider import get_cal_test_use_case

'''
칼 캘던 하클리 (Caledon Hockley)
로즈의 오만한 약혼자. 1등석 승객이자 재력가로 잭과 대립하며 테스트 성격의 악역을 맡음
'''

cal_tester_router = APIRouter(prefix="/cal", tags=["cal"])


@cal_tester_router.get("/myself")
async def introduce_myself(
    cal: CalTestUseCase = Depends(get_cal_test_use_case)
) -> CalTestResponse:
    return await cal.introduce_myself(
        CalTestSchema(
            id=7,
            name="칼 캘던 하클리 (Caledon Hockley)"
        )
    )
