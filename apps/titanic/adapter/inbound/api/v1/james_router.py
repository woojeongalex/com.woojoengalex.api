from fastapi import APIRouter, Depends, File, UploadFile

from titanic.adapter.inbound.api.deps.titanic_deps import get_james_use_case
from titanic.adapter.inbound.api.mappers.james_inbound_mapper import (
    james_schemas_to_person_commands,
)
from titanic.adapter.inbound.api.parsers.james_csv_parser import read_james_upload
from titanic.adapter.inbound.api.schemas.james_schema import JamesUploadResponse
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.dtos.james_command import JamesResponse


james_router = APIRouter(prefix="/titanic/james", tags=["james"])


@james_router.post("/upload", response_model=JamesUploadResponse)
async def upload_titanic_csv(
    file: UploadFile = File(...),
    james: JamesUseCase = Depends(get_james_use_case),
) -> JamesUploadResponse:
    file_name, rows = await read_james_upload(file)
    result = await james.upload(
        james_schemas_to_person_commands(rows),
        file_name,
    )
    return JamesUploadResponse(**result)
