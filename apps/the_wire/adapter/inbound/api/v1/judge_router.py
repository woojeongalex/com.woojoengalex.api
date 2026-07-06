from fastapi import APIRouter, Depends, Query
from the_wire.adapter.inbound.api.mappers.introduce_mapper import (
    dto_to_response_schema,
    schema_to_query,
)
from the_wire.adapter.inbound.api.mappers.judge_mapper import (
    request_to_command,
    result_to_response,
)
from the_wire.adapter.inbound.api.schemas.introduce_schema import (
    IntroduceResponseSchema,
)
from the_wire.adapter.inbound.api.schemas.judge_schema import (
    JudgeRequest,
    JudgeResponse,
)
from the_wire.app.ports.input.judge_use_case import JudgeUseCase
from the_wire.dependencies.judge_provider import get_judge_use_case

judge_router = APIRouter(prefix="/api/the-wire", tags=["the-wire-judge"])


@judge_router.post("/judge", response_model=JudgeResponse)
async def judge_mail(
    req: JudgeRequest,
    use_case: JudgeUseCase = Depends(get_judge_use_case),
) -> JudgeResponse:
    result = use_case.judge(request_to_command(req))
    return result_to_response(result)


@judge_router.get("/judge/myself", response_model=IntroduceResponseSchema)
async def judge_introduce_myself(
    locale: str = Query("ko", description="응답 언어 (ko / en)"),
    use_case: JudgeUseCase = Depends(get_judge_use_case),
) -> IntroduceResponseSchema:
    query = schema_to_query(locale)
    dto = await use_case.introduce_myself(query)
    return dto_to_response_schema(dto)
