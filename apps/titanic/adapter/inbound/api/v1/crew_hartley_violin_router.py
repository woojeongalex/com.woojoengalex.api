from fastapi import APIRouter, Depends

from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.dependencies.crew_hartley_violin_provider import get_hartley_violin_use_case

hartley_violin_router = APIRouter(prefix="/titanic/hartley", tags=["hartley"])


@hartley_violin_router.get("/myself")
async def introduce_myself(
    hartley: HartleyViolinUseCase = Depends(get_hartley_violin_use_case),
):
    return await hartley.introduce_myself()
