from dataclasses import dataclass


@dataclass(frozen=True)
class VocalEvaluationCreateCommand:
    pitch_score: int
    rhythm_score: int
    vocal_grade: str
    summary: str
    catalog_song_id: str | None
    mr_search_list_id: int | None
    input_source: str
    file_name: str
    duration_sec: int


@dataclass(frozen=True)
class VocalEvaluationResultDto:
    id: int
    ok: bool = True
    message: str = "저장되었습니다."
