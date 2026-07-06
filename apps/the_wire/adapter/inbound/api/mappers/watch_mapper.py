from the_wire.adapter.inbound.api.schemas.inbox_schemas import ReceiveMailRequest
from the_wire.adapter.inbound.api.schemas.watch_schemas import (
    PolicyFilterResponse,
    WatchStatusResponse,
)
from the_wire.app.dtos.watch_dto import (
    PolicyFilterCommand,
    PolicyFilterResult,
    WatchStatusResult,
)


def result_to_response(r: WatchStatusResult) -> WatchStatusResponse:
    return WatchStatusResponse(
        history_id=r.history_id,
        expiration=r.expiration,
        updated_at=r.updated_at,
    )


def inbox_request_to_filter_command(req: ReceiveMailRequest) -> PolicyFilterCommand:
    return PolicyFilterCommand(
        sender=req.sender,
        subject=req.subject,
        body=req.body,
    )


def filter_result_to_response(r: PolicyFilterResult) -> PolicyFilterResponse:
    return PolicyFilterResponse(verdict=r.verdict, score=r.score, reason=r.reason)
