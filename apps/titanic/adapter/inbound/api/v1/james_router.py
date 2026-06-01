import csv
import io
import logging

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from pydantic import ValidationError

from titanic.adapter.inbound.api.deps.titanic_deps import get_james_use_case
from titanic.adapter.inbound.api.handlers.titanic_inbound_handlers import pass_james_upload
from titanic.adapter.inbound.api.schemas.james_schema import (
    JAMES_CSV_COLUMNS,
    JamesSchema,
    JamesUploadResponse,
    has_james_csv_column,
)
from titanic.app.ports.input.james_use_case import JamesUseCase

logger = logging.getLogger(__name__)

james_router = APIRouter(prefix="/titanic/james", tags=["james"])


@james_router.post("/upload", response_model=JamesUploadResponse)
async def upload_titanic_csv(
    request: Request,
    file: UploadFile = File(...),
    james: JamesUseCase = Depends(get_james_use_case),
) -> JamesUploadResponse:
    _ = request
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="업로드 파일이 비어 있습니다.")

    file_name = file.filename or "upload.csv"
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더가 없습니다.")

    fieldnames = list(reader.fieldnames)
    missing = [
        col for col in JAMES_CSV_COLUMNS if not has_james_csv_column(col, fieldnames)
    ]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"필수 컬럼이 없습니다: {', '.join(missing)}",
        )

    records = list(reader)
    if not records:
        raise HTTPException(status_code=400, detail="CSV에 데이터 행이 없습니다.")

    try:
        rows: list[JamesSchema] = [
            JamesSchema.model_validate(row) for row in records
        ]
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors()) from exc

    logger.info(
        "[제임스 라우터] 업로드 된 csv파일에서 파싱 완료 — 전체 %s건 (아래 상위 5개만 표시)",
        len(rows),
    )
    for index, record in enumerate(rows[:5], start=1):
        logger.info("[제임스 라우터] preview %s: %s", index, record.model_dump())

    return await pass_james_upload(james, file_name, rows)