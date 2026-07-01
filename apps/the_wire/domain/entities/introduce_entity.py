from dataclasses import dataclass


@dataclass(frozen=True)
class IntroduceEntity:
    agent_name: str
    role: str
    capabilities: list[str]
    version: str
