from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from pydantic import ValidationError

from titanic.adapter.inbound.api.deps.titanic_deps import get_james_use_case
from titanic.adapter.inbound.api.handlers.titanic_inbound_handlers import pass_james_upload
from titanic.adapter.inbound.api.parsers.james_csv_parser import JamesCsvError, parse_james_csv
from titanic.adapter.inbound.api.schemas.james_schema import JamesSchema, JamesUploadResponse
from titanic.app.ports.input.james_use_case import JamesUseCase

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

    try:
        rows: list[JamesSchema] = parse_james_csv(raw.decode("utf-8-sig"))
    except JamesCsvError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors()) from exc

    print(f"[제임스 라우터] JamesSchema {len(rows)}건, 상위 5개:")
    for row in rows[:5]:
        print(row.model_dump())

    response = await pass_james_upload(james, file.filename or "upload.csv", rows)
    print("[제임스 라우터] 업로드 결과:", response)
    return response
