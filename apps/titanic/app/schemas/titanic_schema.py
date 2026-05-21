from pydantic import BaseModel, Field


class TitanicCountResponse(BaseModel):
    count: int


class TitanicSurvivedCountResponse(BaseModel):
    survived_count: int


class TitanicDeadCountResponse(BaseModel):
    dead_count: int


class TitanicTreeResponse(BaseModel):
    tree: bool


class TitanicModelMetricsResponse(BaseModel):
    model_name: str
    accuracy: float = Field(ge=0.0, le=1.0)


class TitanicColumnInfo(BaseModel):
    name: str
    description: str
    dtype: str
    notes: str = ""


class TitanicDatasetSchemaResponse(BaseModel):
    """데이터셋 컬럼 메타 (배너·문서용)."""
    columns: list[TitanicColumnInfo]
    ml_features: list[str]
    ml_target: str
