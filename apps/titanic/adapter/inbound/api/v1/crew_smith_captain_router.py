from fastapi import APIRouter, Depends

from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.dependencies.crew_smith_captain_provider import get_smith_captain_use_case

smith_captain_router = APIRouter(prefix="/titanic/smith", tags=["smith"])


@smith_captain_router.get("/myself")
async def introduce_myself(
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
):
    return await smith.introduce_myself()
