from dataclasses import dataclass


@dataclass(frozen=True)
class VocalRecommendationCreateCommand:
    sing_evaluation_id: int


@dataclass(frozen=True)
class VocalRecommendationResultDto:
    id: int
    sing_evaluation_id: int
    pitch_score_snapshot: int
    rhythm_score_snapshot: int
    vocal_grade_snapshot: str
    vocalization_pattern: str
    recommended_genres: list[str]
    recommended_songs: list[str]
