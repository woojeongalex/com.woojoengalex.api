import base64
import json

from the_wire.adapter.inbound.api.schemas.receiver_schemas import PubSubPushRequest


def decode_pubsub_payload(req: PubSubPushRequest) -> dict:
    decoded = base64.b64decode(req.message.data).decode("utf-8")
    return json.loads(decoded)
