from dataclasses import dataclass


@dataclass(frozen=True)
class SaveContactCommand:
    name: str
    email: str


@dataclass(frozen=True)
class SearchContactQuery:
    q: str


@dataclass(frozen=True)
class ContactResult:
    name: str
    email: str


@dataclass(frozen=True)
class UploadContactsResult:
    saved: int
    skipped: int
