from the_wire.adapter.outbound.orm.contact_model import ContactModel
from the_wire.app.dtos.contact_dto import ContactResult, SaveContactCommand


def command_to_model(command: SaveContactCommand) -> ContactModel:
    return ContactModel(name=command.name, email=command.email)


def model_to_result(model: ContactModel) -> ContactResult:
    return ContactResult(name=model.name, email=model.email)
