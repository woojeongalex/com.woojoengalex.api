from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class HubNode:
    """스타 토폴로지의 중앙 허브 노드.

    허브는 연결된 스포크들의 레지스트리를 보유하고,
    모든 컨텍스트 라우팅의 진입점 역할을 한다.
    """

    id: int
    name: str
    description: str
    spoke_ids: list[int] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True

    def register_spoke(self, spoke_id: int) -> None:
        if spoke_id not in self.spoke_ids:
            self.spoke_ids.append(spoke_id)

    def unregister_spoke(self, spoke_id: int) -> None:
        self.spoke_ids = [s for s in self.spoke_ids if s != spoke_id]

    def spoke_count(self) -> int:
        return len(self.spoke_ids)
