from the_wire.adapter.inbound.api.schemas.contact_schemas import (
    ContactResponse,
    ContactSaveRequest,
)
from the_wire.app.dtos.contact_dto import (
    ContactResult,
    SaveContactCommand,
    SearchContactQuery,
)


def to_save_command(req: ContactSaveRequest) -> SaveContactCommand:
    return SaveContactCommand(name=req.name, email=req.email)


def to_search_query(q: str) -> SearchContactQuery:
    return SearchContactQuery(q=q)


def to_response(result: ContactResult) -> ContactResponse:
    return ContactResponse(name=result.name, email=result.email)
