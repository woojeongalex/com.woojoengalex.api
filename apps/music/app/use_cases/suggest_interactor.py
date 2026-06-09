import logging
from collections.abc import Callable
from dataclasses import dataclass

from music.app.catalog import VOCAL_CATALOG
from music.adapter.outbound.orm.ai_vocal_analysis_model import AiVocalAnalysisEntity
from music.adapter.outbound.orm.suggest_model import VocalRecommendationEntity
from music.app.dtos.suggest_dto import (
    VocalRecommendationCreateCommand,
    VocalRecommendationResultDto,
)
from music.app.ports.input.suggest_use_case import SuggestUseCase
from music.app.ports.output.suggest_repository_port import SuggestRepositoryPort

logger = logging.getLogger(__name__)


@dataclass
class _VocalRule:
    predicate: Callable[[int, int, str], bool]
    genres: list[str]
    song_keys: tuple[str, str]
    pattern: str

    def matches(self, pitch: int, rhythm: int, summary_lower: str) -> bool:
        return self.predicate(pitch, rhythm, summary_lower)


_VOCAL_RULES: list[_VocalRule] = [
    _VocalRule(
        predicate=lambda p, r, _: p >= 88 and r >= 88,
        genres=["발라드", "뮤지컬 넘버"],
        song_keys=("night_letter", "defying"),
        pattern=(
            "음정 안정성과 박자 정확도가 모두 높습니다. 감성 발라드와 뮤지컬 넘버로 "
            "호흡·발성 표현을 넓혀 보세요."
        ),
    ),
    _VocalRule(
        predicate=lambda p, r, _: p >= 75 and r >= 75,
        genres=["발라드", "어쿠스틱 팝"],
        song_keys=("night_letter", "spring"),
        pattern="음정·박자 균형이 안정적인 편입니다. 서정적인 장르에서 발성 패턴을 다듬기 좋습니다.",
    ),
    _VocalRule(
        predicate=lambda p, _, s: p >= 60 or "호흡" in s or "발성" in s,
        genres=["R&B", "발라드"],
        song_keys=("spring", "night_letter"),
        pattern="리듬·감성 표현을 보완하면 좋습니다. 짧은 구간 위주로 음정·박자를 맞춰 보세요.",
    ),
    _VocalRule(
        predicate=lambda p, r, s: True,
        genres=["팝", "어쿠스틱"],
        song_keys=("spring", "defying"),
        pattern="연습량을 늘리며 음정 구간을 나눠 연습해 보세요. 장르별 발성 루틴을 추천합니다.",
    ),
]


def _resolve_catalog_songs() -> dict[str, str]:
    titles = [i.title for i in VOCAL_CATALOG]
    return {
        "night_letter": next((t for t in titles if "밤편지" in t), titles[1]),
        "defying": next((t for t in titles if "Defying" in t or "Gravity" in t), "Defying Gravity"),
        "spring": next((t for t in titles if "봄" in t), titles[0]),
    }


def _compose_recommendation(
    ai: AiVocalAnalysisEntity,
) -> tuple[list[str], list[str], str]:
    pitch = ai.pitch_score
    rhythm = ai.rhythm_score
    summary_lower = (ai.summary or "").lower()
    catalog_songs = _resolve_catalog_songs()

    for rule in _VOCAL_RULES:
        if rule.matches(pitch, rhythm, summary_lower):
            songs = [catalog_songs[k] for k in rule.song_keys]
            return rule.genres, songs, rule.pattern

    raise RuntimeError("추천 규칙을 찾을 수 없습니다.")


class SuggestInteractor(SuggestUseCase):
    def __init__(self, repository: SuggestRepositoryPort) -> None:
        self._repository = repository

    async def upload(
        self, command: VocalRecommendationCreateCommand
    ) -> VocalRecommendationResultDto:
        row = await self._repository.get_sing_evaluation_by_id(command.sing_evaluation_id)
        if row is None:
            raise ValueError("해당 보컬 평가가 없습니다.")

        ai = await self._repository.get_ai_analysis_for_sing_evaluation(row.id)
        if ai is None:
            raise ValueError("해당 평가에 대한 AI 분석 결과가 없습니다.")

        genres, songs, pattern = _compose_recommendation(ai)
        if ai.id is None:
            raise ValueError("AI 분석 행 id가 없습니다.")
        entity = VocalRecommendationEntity(
            sing_evaluation_id=row.id,
            ai_vocal_analysis_id=ai.id,
            vocalization_pattern=pattern,
            recommended_genres=genres,
            recommended_songs=songs,
        )
        saved = await self._repository.save_recommendation(entity)
        logger.info(
            "[MUSIC][suggest][4/interactor] 추천 저장 id=%s evaluation_id=%s genres=%s",
            saved.id,
            saved.sing_evaluation_id,
            genres,
        )
        return await _entity_to_dto(self._repository, saved)

    async def read(
        self, sing_evaluation_id: int
    ) -> VocalRecommendationResultDto | None:
        entity = await self._repository.get_latest_by_evaluation_id(sing_evaluation_id)
        if entity is None:
            return None
        return await _entity_to_dto(self._repository, entity)


async def _entity_to_dto(
    repo: SuggestRepositoryPort,
    e: VocalRecommendationEntity,
) -> VocalRecommendationResultDto:
    ai = await repo.get_ai_analysis_by_id(e.ai_vocal_analysis_id)
    if ai is None:
        raise RuntimeError(
            "vocal_recommendations.ai_vocal_analysis_id 가 가리키는 분석 행을 찾을 수 없습니다."
        )
    genres = [str(x) for x in (e.recommended_genres or [])]
    songs = [str(x) for x in (e.recommended_songs or [])]
    return VocalRecommendationResultDto(
        id=e.id,
        sing_evaluation_id=e.sing_evaluation_id,
        pitch_score_snapshot=ai.pitch_score,
        rhythm_score_snapshot=ai.rhythm_score,
        vocal_grade_snapshot=ai.vocal_grade,
        vocalization_pattern=e.vocalization_pattern,
        recommended_genres=genres,
        recommended_songs=songs,
    )
