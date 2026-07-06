from the_wire.app.dtos.inbox_dto import ReceiveMailCommand


def payload_to_command(payload: dict) -> ReceiveMailCommand:
    return ReceiveMailCommand(
        sender=payload.get("emailAddress", ""),
        subject="Gmail Push 알림",
        body=f"historyId={payload.get('historyId', '')}",
    )
