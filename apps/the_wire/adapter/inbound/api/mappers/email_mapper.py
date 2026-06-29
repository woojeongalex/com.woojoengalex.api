from the_wire.adapter.inbound.api.schemas.email_schemas import EmailRequest
from the_wire.app.dtos.email_dto import EmailCommand


def request_to_command(req: EmailRequest) -> EmailCommand:
    return EmailCommand(to=req.to, subject=req.subject, topic=req.topic)
