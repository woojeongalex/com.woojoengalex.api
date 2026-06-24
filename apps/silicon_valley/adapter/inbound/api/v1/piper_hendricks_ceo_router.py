from fastapi import APIRouter, Depends

from silicon_valley.adapter.inbound.api.schemas.piper_hendricks_ceo_schema import HendricksCeoSchema
from silicon_valley.app.dtos.piper_hendricks_ceo_dto import HendricksCeoResponse
from silicon_valley.app.ports.input.piper_hendricks_ceo_use_case import HendricksCeoUseCase
from silicon_valley.dependencies.piper_hendricks_ceo_provider import get_hendricks_ceo_use_case
from silicon_valley.dependencies.provider import get_n8n_client

'''
리처드 헨드릭스 (Richard Hendricks)
파이드 파이퍼의 CEO이자 창업자. 천재 개발자로 중간값 압축 알고리즘을 개발했지만 사회성은 부족한 인물.
'''
hendricks_ceo_router = APIRouter(prefix="/hendricks", tags=["hendricks"])


@hendricks_ceo_router.get("/myself")
async def introduce_myself(
    hendricks: HendricksCeoUseCase = Depends(get_hendricks_ceo_use_case)
) -> HendricksCeoResponse:
    result = await hendricks.introduce_myself(
        HendricksCeoSchema(
            id=5,
            name="리처드 헨드릭스 (Richard Hendricks)"
        )
    )
    n8n = get_n8n_client()
    await n8n.send_event({"message": "리처드 헨드릭스가 자기소개를 했습니다."})
    return result
