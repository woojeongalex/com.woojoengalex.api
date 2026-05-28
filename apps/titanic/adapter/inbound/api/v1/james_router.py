import csv
import logging
from io import StringIO

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from titanic.adapter.inbound.api.schemas.titanic_request import TitanicCommandRequest
from titanic.app.ports.input.james_use_case import build_james_use_case
from titanic.app.titanic_flow_log import titanic_flow_log

logger = logging.getLogger(__name__)

james_router = APIRouter(prefix="/titanic/james", tags=["james"])


@james_router.post("/upload")
@james_router.post("/fileupload")
async def upload_titanic_csv(
    request: Request,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    origin = request.headers.get("x-flow-origin", "unknown")
    titanic_flow_log(
        "james-upload",
        "1/frontend->inbound",
        "origin=%s file=%s",
        origin,
        file.filename,
    )

    try:
        raw = await file.read()
        decoded = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="CSV 인코딩은 UTF-8 이어야 합니다.") from exc

    reader = csv.DictReader(StringIO(decoded))
    required_columns = {
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
    header = set(reader.fieldnames or [])
    has_sex = "Sex" in header
    has_gender = "gender" in header
    if not has_sex and not has_gender:
        raise HTTPException(status_code=400, detail="필수 컬럼이 없습니다: Sex 또는 gender")
    missing = sorted(required_columns - header)
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"필수 컬럼이 없습니다: {', '.join(missing)}",
        )

    records: list[TitanicCommandRequest] = []
    for row_index, row in enumerate(reader, start=2):
        if not any((value or "").strip() for value in row.values()):
            continue
        if "Sex" not in row and "gender" in row:
            row["Sex"] = row["gender"]
        try:
            command = TitanicCommandRequest.model_validate(row)
        except ValidationError as exc:
            raise HTTPException(
                status_code=400,
                detail=f"{row_index}행 데이터 형식이 올바르지 않습니다: {exc.errors()}",
            ) from exc
        records.append(command)

    titanic_flow_log(
        "james-upload",
        "1/inbound",
        "parsed rows=%s to=input-port",
        len(records),
    )

    try:
        result = await build_james_use_case(db).receive_uploaded_rows(
            file.filename,
            records,
        )
        titanic_flow_log(
            "james-upload",
            "1/inbound",
            "response count=%s to=frontend",
            result.get("count", 0),
        )
        return result
    except SQLAlchemyError as exc:
        logger.exception(
            "[TITANIC-FLOW][james-upload][1/inbound] DB 저장 실패 file=%s rows=%s error=%s",
            file.filename,
            len(records),
            exc,
        )
        raise HTTPException(
            status_code=503,
            detail="DB 저장에 실패했습니다. 서버 로그를 확인하세요.",
        ) from exc
