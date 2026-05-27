from fastapi import APIRouter, Depends, HTTPException

from titanic.app.ports.input.titanic_query_port import TitanicQueryPort
from titanic.app.schemas.titanic_schema import TitanicDatasetSchemaResponse
from titanic.app.use_cases.titanic_query_impl import get_titanic_query

titanic_query_router = APIRouter(prefix="/titanic", tags=["titanic"])


@titanic_query_router.get("/data")
def read_titanic_data():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다.",
    )


@titanic_query_router.get("/count")
def read_titanic_count():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다.",
    )


@titanic_query_router.get("/count/survived")
def read_titanic_survived_count():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다.",
    )


@titanic_query_router.get("/count/dead")
def read_titanic_dead_count():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다.",
    )


@titanic_query_router.get("/tree")
def read_titanic_tree():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다.",
    )


@titanic_query_router.get("/schema", response_model=TitanicDatasetSchemaResponse)
def read_titanic_schema(
    query: TitanicQueryPort = Depends(get_titanic_query),
) -> TitanicDatasetSchemaResponse:
    """데이터셋 컬럼 설명·ML 피처 목록."""
    return query.get_dataset_schema()


@titanic_query_router.get("/model")
def read_titanic_model():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다.",
    )
