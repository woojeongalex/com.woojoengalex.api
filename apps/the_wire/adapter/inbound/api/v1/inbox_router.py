from fastapi import APIRouter, Depends
from the_wire.adapter.inbound.api.mappers.inbox_mapper import (
    request_to_command,
    result_to_response,
)
from the_wire.adapter.inbound.api.schemas.inbox_schemas import (
    InboxListResponse,
    InboxMailResponse,
    ReceiveMailRequest,
)
from the_wire.app.ports.input.inbox_use_case import InboxUseCase
from the_wire.dependencies.inbox_provider import get_inbox_use_case

inbox_router = APIRouter(prefix="/api/the-wire", tags=["the-wire-inbox"])


@inbox_router.post("/inbox", response_model=InboxMailResponse)
async def receive_mail(
    req: ReceiveMailRequest,
    use_case: InboxUseCase = Depends(get_inbox_use_case),
) -> InboxMailResponse:
    result = await use_case.receive(request_to_command(req))
    return result_to_response(result)


@inbox_router.get("/inbox", response_model=InboxListResponse)
async def list_inbox(
    use_case: InboxUseCase = Depends(get_inbox_use_case),
) -> InboxListResponse:
    results = await use_case.list_inbox()
    return InboxListResponse(mails=[result_to_response(r) for r in results])
