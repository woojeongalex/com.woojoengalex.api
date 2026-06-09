from fastapi import APIRouter, Depends

from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.dependencies.crew_lowe_boat_provider import get_lowe_boat_use_case

lowe_boat_router = APIRouter(prefix="/titanic/lowe", tags=["lowe"])


@lowe_boat_router.get("/myself")
async def introduce_myself(
    lowe: LoweBoatUseCase = Depends(get_lowe_boat_use_case),
):
    return await lowe.introduce_myself()
