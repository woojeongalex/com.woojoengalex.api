from fastapi import APIRouter, Depends

from music.adapter.inbound.api.deps.music_deps import get_evaluation_use_case
from music.adapter.inbound.api.handlers.evaluation_inbound_handlers import pass_sing_evaluation
from music.adapter.inbound.api.mappers.music_inbound_mapper import (
    from_evaluation_create,
    to_evaluation_response,
)
from music.adapter.inbound.api.schemas.sing_schema import (
    SingEvaluationCreateRequest,
    SingEvaluationResponse,
)
from music.app.ports.input.evaluation_use_case import EvaluationUseCase

evaluation_router = APIRouter(tags=["music-evaluation"])


@evaluation_router.post("/api/music/sing-evaluation", response_model=SingEvaluationResponse)
async def post_sing_evaluation(
    body: SingEvaluationCreateRequest,
    evaluation: EvaluationUseCase = Depends(get_evaluation_use_case),
) -> SingEvaluationResponse:
    result = await pass_sing_evaluation(evaluation, from_evaluation_create(body))
    return to_evaluation_response(result)
