from the_wire.adapter.inbound.api.schemas.inbox_schemas import (
    InboxMailResponse,
    ReceiveMailRequest,
)
from the_wire.app.dtos.inbox_dto import InboxResult, ReceiveMailCommand


def request_to_command(req: ReceiveMailRequest) -> ReceiveMailCommand:
    return ReceiveMailCommand(sender=req.sender, subject=req.subject, body=req.body)


def result_to_response(r: InboxResult) -> InboxMailResponse:
    return InboxMailResponse(
        id=r.id,
        sender=r.sender,
        subject=r.subject,
        body=r.body,
        received_at=r.received_at,
        is_read=r.is_read,
    )
