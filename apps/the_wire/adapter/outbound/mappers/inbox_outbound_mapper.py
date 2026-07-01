from the_wire.adapter.outbound.orm.inbox_model import InboxModel
from the_wire.app.dtos.inbox_dto import InboxResult, ReceiveMailCommand


def command_to_model(command: ReceiveMailCommand) -> InboxModel:
    return InboxModel(
        sender=command.sender,
        subject=command.subject,
        body=command.body,
    )


def model_to_result(model: InboxModel) -> InboxResult:
    return InboxResult(
        id=model.id,
        sender=model.sender,
        subject=model.subject,
        body=model.body,
        received_at=model.received_at,
        is_read=model.is_read,
    )
