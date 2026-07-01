from dataclasses import dataclass


@dataclass(frozen=True)
class ContactEntity:
    name: str
    email: str
