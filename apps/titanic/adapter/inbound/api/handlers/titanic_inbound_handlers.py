"""Titanic inbound — HTTP·DB 경계 (라우터는 Use Case만 호출)."""

from fastapi import Request

from titanic.adapter.inbound.api.schemas.james_schema import JamesSchema, JamesUploadResponse
from titanic.app.titanic_flow_log import titanic_flow_log
from titanic.adapter.inbound.api.schemas.titanic_schema import (
    WalterPassengerItem,
    WalterPassengerPageResponse,
)
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.input.walter_use_case import WalterUseCase


async def pass_james_upload(
    james: type[JamesUseCase],
    file_name: str,
    rows: list[JamesSchema],
) -> JamesUploadResponse:
    payload = [row.to_passenger_row_dict() for row in rows]
    result = await james.receive_uploaded_records(payload, file_name)
    titanic_flow_log(
        "james-upload",
        "inbound",
        "Neon 저장 완료 file=%s saved=%s",
        file_name,
        result.get("count", len(rows)) if isinstance(result, dict) else len(rows),
        source_file=file_name,
    )
    if isinstance(result, dict):
        return JamesUploadResponse(**result)
    return JamesUploadResponse(file_name=file_name, count=len(rows))


async def handle_walter_read(
    request: Request,
    source_file: str | None,
    page: int,
    size: int,
    walter: type[WalterUseCase],
) -> WalterPassengerPageResponse:
    _ = request
    data = await walter.read_passengers(source_file, page, size)
    rows = [WalterPassengerItem(**row) for row in data.get("rows", [])]
    return WalterPassengerPageResponse(
        source_file=data.get("source_file"),
        page=data.get("page", page),
        size=data.get("size", size),
        total=data.get("total", 0),
        total_pages=data.get("total_pages", 0),
        rows=rows,
    )
