from fastapi import APIRouter, Depends, File, Query, UploadFile
from the_wire.adapter.inbound.api.mappers.introduce_mapper import (
    dto_to_response_schema,
    schema_to_query,
)
from the_wire.adapter.inbound.api.parsers.google_contacts_csv_parser import (
    parse_google_contacts_csv,
)
from the_wire.adapter.inbound.api.schemas.contact_schemas import ContactUploadResult
from the_wire.adapter.inbound.api.schemas.introduce_schema import (
    IntroduceResponseSchema,
)
from the_wire.app.ports.input.contact_use_case import ContactUseCase
from the_wire.app.ports.input.introduce_use_case import IntroduceUseCase
from the_wire.dependencies.contact_provider import get_contact_use_case
from the_wire.dependencies.introduce_provider import get_introduce_use_case

introduce_router = APIRouter(prefix="/api/the-wire", tags=["the-wire"])


@introduce_router.get("/introduce", response_model=IntroduceResponseSchema)
async def introduce_myself(
    locale: str = Query("ko", description="응답 언어 (ko / en)"),
    use_case: IntroduceUseCase = Depends(get_introduce_use_case),
) -> IntroduceResponseSchema:
    query = schema_to_query(locale)
    dto = await use_case.introduce_myself(query)
    return dto_to_response_schema(dto)


@introduce_router.post("/introduce/upload", response_model=ContactUploadResult)
async def upload_google_contacts_csv(
    file: UploadFile = File(...),
    contact: ContactUseCase = Depends(get_contact_use_case),
) -> ContactUploadResult:
    commands = await parse_google_contacts_csv(file)
    result = await contact.upload(commands)
    return ContactUploadResult(saved=result.saved, skipped=result.skipped)
