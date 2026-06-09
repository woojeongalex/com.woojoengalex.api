"""James upload CSV → `JamesSchema` 목록 (무상태 파싱)."""

import csv
import io

from fastapi import HTTPException, UploadFile
from pydantic import ValidationError

from titanic.adapter.inbound.api.schemas.crew_james_schema import (
    JAMES_CSV_COLUMNS,
    JamesSchema,
    has_james_csv_column,
)

JAMES_UPLOAD_CONTENT_TYPES = frozenset(
    {"text/csv", "application/vnd.ms-excel", "text/plain"}
)


class JamesCsvError(ValueError):
    pass


def parse_james_csv(text: str) -> list[JamesSchema]:
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise JamesCsvError("CSV 헤더가 없습니다.")

    fieldnames = list(reader.fieldnames)
    missing = [
        col for col in JAMES_CSV_COLUMNS if not has_james_csv_column(col, fieldnames)
    ]
    if missing:
        raise JamesCsvError(f"필수 컬럼이 없습니다: {', '.join(missing)}")

    records = list(reader)
    if not records:
        raise JamesCsvError("CSV에 데이터 행이 없습니다.")

    try:
        return [JamesSchema.model_validate(row) for row in records]
    except ValidationError:
        raise


async def read_james_upload(file: UploadFile) -> tuple[str, list[JamesSchema]]:
    """업로드 파일 검증·디코딩·CSV 파싱 (무상태). 실패 시 HTTP 400."""
    if file.content_type not in JAMES_UPLOAD_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="CSV 파일을 업로드해주세요.")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="업로드 파일이 비어 있습니다.")

    try:
        rows = parse_james_csv(raw.decode("utf-8-sig", errors="replace"))
    except JamesCsvError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors()) from exc

    return file.filename or "upload.csv", rows
