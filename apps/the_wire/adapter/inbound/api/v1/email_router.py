from fastapi import APIRouter, Depends
from the_wire.adapter.inbound.api.deps.the_wire_deps import get_email_use_case
from the_wire.adapter.inbound.api.mappers.email_mapper import request_to_command
from the_wire.adapter.inbound.api.schemas.email_schemas import (
    EmailRequest,
    EmailResponse,
)
from the_wire.app.ports.input.email_use_case import EmailUseCase

the_wire_router = APIRouter(prefix="/api/the-wire", tags=["the-wire"])


@the_wire_router.post("/email", response_model=EmailResponse)
async def send_email(
    req: EmailRequest,
    use_case: EmailUseCase = Depends(get_email_use_case),
) -> EmailResponse:
    result = await use_case.send_email(request_to_command(req))
    return EmailResponse(success=result.success, detail=result.detail)
