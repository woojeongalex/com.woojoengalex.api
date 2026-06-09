from dataclasses import dataclass


@dataclass(frozen=True)
class JackTrainQuery:
    id: int
    name: str


@dataclass(frozen=True)
class JackTrainResponse:
    id: int
    name: str
    role: str = ""
    description: str = ""
    ability: str = ""
