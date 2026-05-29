from fastapi import APIRouter

from titanic.adapter.inbound.api.schemas.dataset_columns import (
    EXTRA_CSV_COLUMNS,
    ML_FEATURE_COLUMNS,
    ML_TARGET_COLUMN,
    TITANIC_COLUMN_SPECS,
)
from titanic.adapter.inbound.api.schemas.titanic_schema import (
    TitanicColumnInfo,
    TitanicDatasetSchemaResponse,
)

rose_router = APIRouter(prefix="/titanic", tags=["titanic"])


@rose_router.get("/schema", response_model=TitanicDatasetSchemaResponse)
def read_titanic_schema() -> TitanicDatasetSchemaResponse:
    """데이터셋 컬럼 설명·ML 피처 목록."""
    specs = TITANIC_COLUMN_SPECS + EXTRA_CSV_COLUMNS
    return TitanicDatasetSchemaResponse(
        columns=[TitanicColumnInfo(**spec) for spec in specs],
        ml_features=list(ML_FEATURE_COLUMNS),
        ml_target=ML_TARGET_COLUMN,
    )
