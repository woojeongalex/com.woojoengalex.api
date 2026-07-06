from fastapi import APIRouter, Depends
from the_wire.adapter.inbound.api.mappers.receiver_mapper import payload_to_command
from the_wire.adapter.inbound.api.parsers.pubsub_payload_parser import (
    decode_pubsub_payload,
)
from the_wire.adapter.inbound.api.schemas.receiver_schemas import (
    PubSubPushRequest,
    ReceiverAckResponse,
)
from the_wire.app.ports.input.inbox_use_case import InboxUseCase
from the_wire.dependencies.inbox_provider import get_inbox_use_case

receiver_router = APIRouter(prefix="/api/the-wire", tags=["the-wire-receiver"])


@receiver_router.post("/receiver", response_model=ReceiverAckResponse)
async def receive_pubsub_push(
    req: PubSubPushRequest,
    use_case: InboxUseCase = Depends(get_inbox_use_case),
) -> ReceiverAckResponse:
    payload = decode_pubsub_payload(req)
    await use_case.receive(payload_to_command(payload))
    return ReceiverAckResponse(status="ok")
