"""HTTP 스키마 ↔ app DTO."""

from dataclasses import asdict

from titanic.adapter.inbound.api.schemas.titanic_request import PassengerCsvRow
from titanic.adapter.inbound.api.schemas.titanic_schema import (
    WalterPassengerItem,
    WalterPassengerPageResponse,
)
from titanic.app.dtos.passenger_row import PassengerRowDto
from titanic.app.dtos.upload_result import UploadResultDto
from titanic.app.dtos.walter_page import WalterPassengerPageDto


def csv_row_to_passenger(csv_row: PassengerCsvRow) -> PassengerRowDto:
    return PassengerRowDto(**csv_row.model_dump(by_alias=False))


def upload_result_to_json(result: UploadResultDto) -> dict[str, str | int]:
    return {"file_name": result.file_name, "count": result.count}


def passenger_page_to_response(page: WalterPassengerPageDto) -> WalterPassengerPageResponse:
    body = asdict(page)
    body["rows"] = [WalterPassengerItem(**asdict(item)) for item in page.rows]
    return WalterPassengerPageResponse(**body)


def passenger_page_dict_to_response(page: dict[str, object]) -> WalterPassengerPageResponse:
    rows = page.get("rows", [])
    return WalterPassengerPageResponse(
        source_file=page.get("source_file"),  # type: ignore[arg-type]
        page=int(page.get("page", 1)),
        size=int(page.get("size", 30)),
        total=int(page.get("total", 0)),
        total_pages=int(page.get("total_pages", 0)),
        rows=[WalterPassengerItem(**row) for row in rows],  # type: ignore[arg-type]
    )
