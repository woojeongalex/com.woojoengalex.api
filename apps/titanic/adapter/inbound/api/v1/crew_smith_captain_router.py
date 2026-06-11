from typing import Annotated

from fastapi import APIRouter, Depends, Body

import titanic.adapter.inbound.api.schemas.crew_smith_captain_schema
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.dependencies.crew_smith_captain_provider import get_smith_captain_use_case
from woojeongai.apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse

smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])


@smith_captain_router.post("/chat")
async def chat(
    schema: Annotated[titanic.adapter.inbound.api.schemas.crew_smith_captain_schema.ChatSchema, Body()],
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
) -> SmithCaptainResponse:
    return await smith.chat(schema)


@smith_captain_router.get("/myself")
async def introduce_myself(
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
):
    return await smith.introduce_myself(
        titanic.adapter.inbound.api.schemas.crew_smith_captain_schema.SmithCaptainSchema(id=2, name="에드워드 존 스미스 (Captain Edward John Smith)")
    )

