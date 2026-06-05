from fastapi import APIRouter, Depends, Query

from music.adapter.inbound.api.deps.music_deps import get_suggest_use_case
from music.adapter.inbound.api.handlers.suggest_inbound_handlers import (
    pass_vocal_recommendation_read,
    pass_vocal_recommendation_upload,
)
from music.adapter.inbound.api.mappers.music_inbound_mapper import (
    from_suggest_create,
    to_suggest_response,
)
from music.adapter.inbound.api.schemas.suggest_schema import (
    VocalRecommendationCreateRequest,
    VocalRecommendationResponse,
)
from music.app.ports.input.suggest_use_case import SuggestUseCase

suggest_router = APIRouter(tags=["music-suggest"])


@suggest_router.post("/api/music/vocal-recommendations", response_model=VocalRecommendationResponse)
async def post_vocal_recommendations(
    body: VocalRecommendationCreateRequest,
    suggest: SuggestUseCase = Depends(get_suggest_use_case),
) -> VocalRecommendationResponse:
    result = await pass_vocal_recommendation_upload(suggest, from_suggest_create(body))
    return to_suggest_response(result)


@suggest_router.get("/api/music/vocal-recommendations", response_model=VocalRecommendationResponse)
async def get_vocal_recommendations(
    singEvaluationId: int = Query(
        ...,
        ge=1,
        alias="singEvaluationId",
        description="sing_evaluations.id",
    ),
    suggest: SuggestUseCase = Depends(get_suggest_use_case),
) -> VocalRecommendationResponse:
    dto = await pass_vocal_recommendation_read(suggest, singEvaluationId)
    return to_suggest_response(dto)
