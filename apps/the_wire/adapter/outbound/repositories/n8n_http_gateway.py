import base64
import os

import httpx
from the_wire.app.dtos.email_dto import EmailCommand, EmailResult
from the_wire.app.ports.output.n8n_gateway_port import N8nGatewayPort

_WEBHOOK_URL = os.getenv("N8N_THE_WIRE_WEBHOOK_URL", "")


def _encode_subject(subject: str) -> str:
    encoded = base64.b64encode(subject.encode()).decode()
    return f"=?UTF-8?B?{encoded}?="


class N8nHttpGateway(N8nGatewayPort):
    async def send(self, command: EmailCommand, body: str) -> EmailResult:
        payload = {"to": command.to, "subject": _encode_subject(command.subject), "body": body}
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            return EmailResult(success=True, detail="sent")
        return EmailResult(success=False, detail=response.text)
