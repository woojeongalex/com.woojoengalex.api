import csv
import logging
from io import StringIO

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from titanic.adapter.inbound.api.deps.titanic_deps import build_james_use_case
from titanic.adapter.inbound.api.mappers.passenger_mapper import (
    csv_row_to_passenger,
    upload_result_to_json,
)
from titanic.adapter.inbound.api.schemas.titanic_request import PassengerCsvRow
from titanic.app.titanic_flow_log import titanic_flow_log

logger = logging.getLogger(__name__)

james_router = APIRouter(prefix="/titanic/james", tags=["james"])

_REQUIRED_COLUMNS = frozenset(
    {
        "PassengerId",
        "Survived",
        "Pclass",
        "Name",
        "Age",
        "SibSp",
        "Parch",
        "Ticket",
        "Fare",
    }
)


def _parse_csv(csv_text: str) -> list[PassengerCsvRow]:
    reader = csv.DictReader(StringIO(csv_text))
    headers = set(reader.fieldnames or [])
    if "Sex" not in headers and "gender" not in headers:
        raise HTTPException(status_code=400, detail="필수 컬럼이 없습니다: Sex 또는 gender")
    missing = sorted(_REQUIRED_COLUMNS - headers)
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"필수 컬럼이 없습니다: {', '.join(missing)}",
        )

    rows: list[PassengerCsvRow] = []
    for line_no, raw_row in enumerate(reader, start=2):
        if not any((cell or "").strip() for cell in raw_row.values()):
            continue
        if "Sex" not in raw_row and "gender" in raw_row:
            raw_row["Sex"] = raw_row["gender"]
        try:
            rows.append(PassengerCsvRow.model_validate(raw_row))
        except ValidationError as exc:
            raise HTTPException(
                status_code=400,
                detail=f"{line_no}행 데이터 형식이 올바르지 않습니다: {exc.errors()}",
            ) from exc
    return rows


@james_router.post("/upload")
async def upload_titanic_csv(
    request: Request,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    try:
        csv_text = (await file.read()).decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="CSV 인코딩은 UTF-8 이어야 합니다.") from exc

    csv_rows = _parse_csv(csv_text)
    passengers = [csv_row_to_passenger(row) for row in csv_rows]

    titanic_flow_log(
        "james-upload",
        "inbound",
        "origin=%s rows=%s",
        request.headers.get("x-flow-origin", "unknown"),
        len(passengers),
        source_file=file.filename or "upload.csv",
    )

    try:
        result = await build_james_use_case(db).save_upload(file.filename, passengers)
        return upload_result_to_json(result)
    except SQLAlchemyError as exc:
        logger.exception(
            "[TITANIC-FLOW][james-upload][inbound] source_file=%s | DB 저장 실패 rows=%s",
            file.filename or "upload.csv",
            len(passengers),
        )
        raise HTTPException(
            status_code=503,
            detail="DB 저장에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
