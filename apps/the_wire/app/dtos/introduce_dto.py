from dataclasses import dataclass, field


@dataclass(frozen=True)
class IntroduceQuery:
    locale: str = "ko"


@dataclass(frozen=True)
class IntroduceResponse:
    agent_name: str
    role: str
    capabilities: list[str] = field(default_factory=list)
    version: str = "1.0.0"
