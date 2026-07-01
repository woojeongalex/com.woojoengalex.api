from pydantic import BaseModel


class ContactSaveRequest(BaseModel):
    name: str
    email: str


class ContactResponse(BaseModel):
    name: str
    email: str


class ContactListResponse(BaseModel):
    contacts: list[ContactResponse]


class ContactUploadResult(BaseModel):
    saved: int
    skipped: int
