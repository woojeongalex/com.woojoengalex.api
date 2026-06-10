from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.dependencies.crew_smith_captain_provider import get_smith_captain_use_case

smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])


@smith_captain_router.post("/chat")
async def chat(
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
):
    return None


@smith_captain_router.get("/myself")
async def introduce_myself(
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
):
    return await smith.introduce_myself(
        SmithCaptainSchema(id=2, name="에드워드 존 스미스 (Captain Edward John Smith)")
    )

