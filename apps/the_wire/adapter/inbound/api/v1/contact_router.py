from fastapi import APIRouter, Depends, Query
from the_wire.adapter.inbound.api.mappers.contact_mapper import (
    to_response,
    to_save_command,
    to_search_query,
)
from the_wire.adapter.inbound.api.schemas.contact_schemas import (
    ContactListResponse,
    ContactResponse,
    ContactSaveRequest,
)
from the_wire.app.ports.input.contact_use_case import ContactUseCase
from the_wire.dependencies.the_wire_director import get_contact_use_case

contact_router = APIRouter(prefix="/api/the-wire", tags=["the-wire-contacts"])


@contact_router.post("/contacts", response_model=ContactResponse)
async def save_contact(
    body: ContactSaveRequest,
    use_case: ContactUseCase = Depends(get_contact_use_case),
) -> ContactResponse:
    result = await use_case.save(to_save_command(body))
    return to_response(result)


@contact_router.get("/contacts", response_model=ContactListResponse)
async def search_contacts(
    q: str = Query(..., min_length=1),
    use_case: ContactUseCase = Depends(get_contact_use_case),
) -> ContactListResponse:
    results = await use_case.search(to_search_query(q))
    return ContactListResponse(contacts=[to_response(r) for r in results])
