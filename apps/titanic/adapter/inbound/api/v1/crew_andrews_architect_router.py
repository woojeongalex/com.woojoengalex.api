from fastapi import APIRouter, Depends

from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.dependencies.crew_andrews_architect_provider import get_andrews_architect_use_case

andrews_architect_router = APIRouter(prefix="/titanic/andrews", tags=["andrews"])


@andrews_architect_router.get("/myself")
async def introduce_myself(
    andrews: AndrewsArchitectUseCase = Depends(get_andrews_architect_use_case),
):
    return await andrews.introduce_myself()
