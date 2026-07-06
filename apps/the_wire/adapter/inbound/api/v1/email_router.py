from fastapi import APIRouter, Depends, File, Query, UploadFile
from the_wire.adapter.inbound.api.deps.the_wire_deps import get_email_use_case
from the_wire.adapter.inbound.api.mappers.contact_mapper import (
    to_response,
    to_save_command,
    to_search_query,
)
from the_wire.adapter.inbound.api.mappers.email_mapper import request_to_command
from the_wire.adapter.inbound.api.mappers.inbox_mapper import (
    request_to_command as inbox_request_to_command,
)
from the_wire.adapter.inbound.api.mappers.inbox_mapper import (
    result_to_response as inbox_result_to_response,
)
from the_wire.adapter.inbound.api.mappers.introduce_mapper import (
    dto_to_response_schema,
    schema_to_query,
)
from the_wire.adapter.inbound.api.parsers.contact_csv_parser import parse_contact_csv
from the_wire.adapter.inbound.api.parsers.google_contacts_csv_parser import (
    parse_google_contacts_csv,
)
from the_wire.adapter.inbound.api.schemas.contact_schemas import (
    ContactListResponse,
    ContactResponse,
    ContactSaveRequest,
    ContactUploadResult,
)
from the_wire.adapter.inbound.api.schemas.email_schemas import (
    EmailRequest,
    EmailResponse,
    SentEmailListResponse,
    SentEmailSchema,
)
from the_wire.adapter.inbound.api.schemas.inbox_schemas import (
    InboxListResponse,
    InboxMailResponse,
    ReceiveMailRequest,
)
from the_wire.adapter.inbound.api.schemas.introduce_schema import (
    IntroduceResponseSchema,
)
from the_wire.app.ports.input.contact_use_case import ContactUseCase
from the_wire.app.ports.input.email_use_case import EmailUseCase
from the_wire.app.ports.input.inbox_use_case import InboxUseCase
from the_wire.app.ports.input.introduce_use_case import IntroduceUseCase
from the_wire.dependencies.contact_provider import get_contact_use_case
from the_wire.dependencies.inbox_provider import get_inbox_use_case
from the_wire.dependencies.introduce_provider import get_introduce_use_case

the_wire_router = APIRouter(prefix="/api/the-wire", tags=["the-wire"])


# ── Email ──────────────────────────────────────────────────────────────────────


@the_wire_router.post("/email", response_model=EmailResponse)
async def send_email(
    req: EmailRequest,
    use_case: EmailUseCase = Depends(get_email_use_case),
) -> EmailResponse:
    result = await use_case.send_email(request_to_command(req))
    return EmailResponse(success=result.success, detail=result.detail)


@the_wire_router.get("/sent-emails", response_model=SentEmailListResponse)
async def list_sent_emails(
    use_case: EmailUseCase = Depends(get_email_use_case),
) -> SentEmailListResponse:
    results = await use_case.list_sent()
    return SentEmailListResponse(emails=[SentEmailSchema(**vars(r)) for r in results])


# ── Inbox ──────────────────────────────────────────────────────────────────────


@the_wire_router.post("/inbox", response_model=InboxMailResponse)
async def receive_mail(
    req: ReceiveMailRequest,
    use_case: InboxUseCase = Depends(get_inbox_use_case),
) -> InboxMailResponse:
    result = await use_case.receive(inbox_request_to_command(req))
    return inbox_result_to_response(result)


@the_wire_router.get("/inbox", response_model=InboxListResponse)
async def list_inbox(
    use_case: InboxUseCase = Depends(get_inbox_use_case),
) -> InboxListResponse:
    results = await use_case.list_inbox()
    return InboxListResponse(mails=[inbox_result_to_response(r) for r in results])


# ── Contacts ───────────────────────────────────────────────────────────────────


@the_wire_router.post("/contacts", response_model=ContactResponse)
async def save_contact(
    body: ContactSaveRequest,
    use_case: ContactUseCase = Depends(get_contact_use_case),
) -> ContactResponse:
    result = await use_case.save(to_save_command(body))
    return to_response(result)


@the_wire_router.get("/contacts/all", response_model=ContactListResponse)
async def list_contacts(
    use_case: ContactUseCase = Depends(get_contact_use_case),
) -> ContactListResponse:
    results = await use_case.list_all()
    return ContactListResponse(contacts=[to_response(r) for r in results])


@the_wire_router.get("/contacts", response_model=ContactListResponse)
async def search_contacts(
    q: str = Query(..., min_length=1),
    use_case: ContactUseCase = Depends(get_contact_use_case),
) -> ContactListResponse:
    results = await use_case.search(to_search_query(q))
    return ContactListResponse(contacts=[to_response(r) for r in results])


@the_wire_router.post("/contacts/upload", response_model=ContactUploadResult)
async def upload_contacts_csv(
    file: UploadFile = File(...),
    use_case: ContactUseCase = Depends(get_contact_use_case),
) -> ContactUploadResult:
    commands = await parse_contact_csv(file)
    result = await use_case.upload(commands)
    return ContactUploadResult(saved=result.saved, skipped=result.skipped)


@the_wire_router.post("/contacts/upload/google", response_model=ContactUploadResult)
async def upload_google_contacts_csv(
    file: UploadFile = File(...),
    use_case: ContactUseCase = Depends(get_contact_use_case),
) -> ContactUploadResult:
    commands = await parse_google_contacts_csv(file)
    result = await use_case.upload(commands)
    return ContactUploadResult(saved=result.saved, skipped=result.skipped)


# ── Introduce Myself ───────────────────────────────────────────────────────────


@the_wire_router.get("/introduce", response_model=IntroduceResponseSchema)
async def introduce_myself(
    locale: str = Query("ko", description="응답 언어 (ko / en)"),
    use_case: IntroduceUseCase = Depends(get_introduce_use_case),
) -> IntroduceResponseSchema:
    query = schema_to_query(locale)
    dto = await use_case.introduce_myself(query)
    return dto_to_response_schema(dto)
