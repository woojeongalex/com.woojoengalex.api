from dataclasses import dataclass


@dataclass(frozen=True)
class EmailCommand:
    to: str
    subject: str
    topic: str


@dataclass(frozen=True)
class EmailResult:
    success: bool
    detail: str


@dataclass(frozen=True)
class EmailStorageCommand:
    to: str
    subject: str
    body: str


@dataclass(frozen=True)
class EmailStorageResult:
    id: int


@dataclass(frozen=True)
class SentEmailResult:
    id: int
    recipient: str
    subject: str
    body: str
    sent_at: str
    has_embedding: bool
