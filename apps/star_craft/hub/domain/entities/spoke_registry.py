from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class SpokeStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


@dataclass
class SpokeRegistryEntry:
    """허브에 등록된 스포크 메타데이터.

    Hub는 이 엔티티를 통해 연결된 스포크의 상태와 라우팅 정보를 관리한다.
    스포크 간 직접 참조는 금지되며, 반드시 Hub를 통해 조회해야 한다.
    """

    id: int
    spoke_name: str
    domain_key: str          # 라우팅 키 (예: "music", "titanic")
    endpoint_prefix: str     # FastAPI 라우터 prefix
    status: SpokeStatus = SpokeStatus.PENDING
    registered_at: datetime = field(default_factory=datetime.utcnow)
    tags: list[str] = field(default_factory=list)

    def activate(self) -> None:
        self.status = SpokeStatus.ACTIVE

    def deactivate(self) -> None:
        self.status = SpokeStatus.INACTIVE

    def is_routable(self) -> bool:
        return self.status == SpokeStatus.ACTIVE
