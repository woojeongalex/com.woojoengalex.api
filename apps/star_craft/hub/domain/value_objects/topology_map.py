from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TopologyMap:
    """허브가 보유한 전체 스타 토폴로지 스냅샷 VO.

    허브 → 스포크 연결 구조를 불변 값 객체로 표현한다.
    스포크 간 직접 연결 엣지는 이 맵에 존재할 수 없다 (토폴로지 제약).
    """

    hub_id: int
    # domain_key → spoke_id 매핑
    spoke_map: dict[str, int] = field(default_factory=dict)

    def resolve_spoke(self, domain_key: str) -> int | None:
        return self.spoke_map.get(domain_key)

    def all_domain_keys(self) -> list[str]:
        return list(self.spoke_map.keys())

    def has_spoke(self, domain_key: str) -> bool:
        return domain_key in self.spoke_map

    def spoke_count(self) -> int:
        return len(self.spoke_map)
