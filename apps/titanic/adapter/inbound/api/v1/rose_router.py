from fastapi import APIRouter, HTTPException

from titanic.adapter.inbound.api.schemas.dataset_columns import (
    EXTRA_CSV_COLUMNS,
    ML_FEATURE_COLUMNS,
    ML_TARGET_COLUMN,
    TITANIC_COLUMN_SPECS,
)
from titanic.adapter.inbound.api.schemas.titanic_schema import TitanicDatasetSchemaResponse
from titanic.adapter.inbound.api.schemas.titanic_schema import TitanicColumnInfo

rose_router = APIRouter(prefix="/titanic", tags=["titanic"])


@rose_router.get("/data")
def read_titanic_data():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다.",
    )


@rose_router.get("/count")
def read_titanic_count():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다.",
    )


@rose_router.get("/count/survived")
def read_titanic_survived_count():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다.",
    )


@rose_router.get("/count/dead")
def read_titanic_dead_count():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다.",
    )


@rose_router.get("/tree")
def read_titanic_tree():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다.",
    )


@rose_router.get("/schema", response_model=TitanicDatasetSchemaResponse)
def read_titanic_schema() -> TitanicDatasetSchemaResponse:
    """데이터셋 컬럼 설명·ML 피처 목록."""
    specs = TITANIC_COLUMN_SPECS + EXTRA_CSV_COLUMNS
    return TitanicDatasetSchemaResponse(
        columns=[TitanicColumnInfo(**spec) for spec in specs],
        ml_features=list(ML_FEATURE_COLUMNS),
        ml_target=ML_TARGET_COLUMN,
    )


@rose_router.get("/model")
def read_titanic_model():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다.",
    )
