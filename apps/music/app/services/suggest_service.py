import logging

from sqlalchemy.ext.asyncio import AsyncSession

from music.app.catalog import VOCAL_CATALOG
from music.app.models.sing_model import SingEvaluationEntity
from music.app.models.suggest_model import VocalRecommendationEntity
from music.app.repositories.suggest_repository import SuggestRepository
from music.app.schemas.suggest_schema import (
    VocalRecommendationCreateRequest,
    VocalRecommendationResponse,
)

logger = logging.getLogger(__name__)


def _compose_recommendation(
    evaluation: SingEvaluationEntity,
) -> tuple[list[str], list[str], str]:
    """음정·박자·요약을 바탕으로 장르·곡·발성 설명 생성 (데모 규칙, 이후 ML·LLM으로 교체 가능)."""
    pitch = evaluation.pitch_score
    rhythm = evaluation.rhythm_score
    summary_lower = (evaluation.summary or "").lower()

    titles = [i.title for i in VOCAL_CATALOG]
    night_letter = next((t for t in titles if "밤편지" in t or t == "밤편지"), titles[1])
    defying = next(
        (t for t in titles if "Defying" in t or "Gravity" in t),
        "Defying Gravity",
    )
    spring = next((t for t in titles if "봄" in t), titles[0])

    if pitch >= 88 and rhythm >= 88:
        genres = ["발라드", "뮤지컬 넘버"]
        songs = [night_letter, defying]
        pattern = (
            "음정 안정성과 박자 정확도가 모두 높습니다. 감성 발라드와 뮤지컬 넘버로 "
            "호흡·발성 표현을 넓혀 보세요."
        )
    elif pitch >= 75 and rhythm >= 75:
        genres = ["발라드", "어쿠스틱 팝"]
        songs = [night_letter, spring]
        pattern = (
            "음정·박자 균형이 안정적인 편입니다. 서정적인 장르에서 발성 패턴을 다듬기 좋습니다."
        )
    elif pitch >= 60 or "호흡" in summary_lower or "발성" in summary_lower:
        genres = ["R&B", "발라드"]
        songs = [spring, night_letter]
        pattern = (
            "리듬·감성 표현을 보완하면 좋습니다. 짧은 구간 위주로 음정·박자를 맞춰 보세요."
        )
    else:
        genres = ["팝", "어쿠스틱"]
        songs = [spring, defying]
        pattern = (
            "연습량을 늘리며 음정 구간을 나눠 연습해 보세요. 장르별 발성 루틴을 추천합니다."
        )

    return genres, songs, pattern


class SuggestService:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self._repository = SuggestRepository(db)

    async def create_from_saved_evaluation(
        self, body: VocalRecommendationCreateRequest
    ) -> VocalRecommendationResponse:
        row = await self._repository.get_sing_evaluation_by_id(body.sing_evaluation_id)
        if row is None:
            raise ValueError("해당 보컬 평가가 없습니다.")

        genres, songs, pattern = _compose_recommendation(row)
        entity = VocalRecommendationEntity(
            sing_evaluation_id=row.id,
            pitch_score_snapshot=row.pitch_score,
            rhythm_score_snapshot=row.rhythm_score,
            vocal_grade_snapshot=row.vocal_grade,
            vocalization_pattern=pattern,
            recommended_genres=genres,
            recommended_songs=songs,
        )
        saved = await self._repository.save_recommendation(entity)
        logger.info(
            "[MUSIC][suggest][4/service] 추천 저장 id=%s evaluation_id=%s genres=%s",
            saved.id,
            saved.sing_evaluation_id,
            genres,
        )
        return _entity_to_response(saved)

    async def get_latest(self, sing_evaluation_id: int) -> VocalRecommendationResponse | None:
        entity = await self._repository.get_latest_by_evaluation_id(sing_evaluation_id)
        if entity is None:
            return None
        return _entity_to_response(entity)


def _entity_to_response(
    e: VocalRecommendationEntity,
) -> VocalRecommendationResponse:
    genres = [str(x) for x in (e.recommended_genres or [])]
    songs = [str(x) for x in (e.recommended_songs or [])]
    return VocalRecommendationResponse(
        id=e.id,
        sing_evaluation_id=e.sing_evaluation_id,
        pitch_score_snapshot=e.pitch_score_snapshot,
        rhythm_score_snapshot=e.rhythm_score_snapshot,
        vocal_grade_snapshot=e.vocal_grade_snapshot,
        vocalization_pattern=e.vocalization_pattern,
        recommended_genres=genres,
        recommended_songs=songs,
    )
