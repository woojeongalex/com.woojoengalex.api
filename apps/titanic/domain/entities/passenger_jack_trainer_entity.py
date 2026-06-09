from dataclasses import dataclass
from typing import Literal
from domain.value_objects import PassengerId, PassengerName, Gender, Age, FamilyRelations

@dataclass
class TitanicPassenger:
    """타이타닉 승객 도메인 엔티티 (핵심 비즈니스 중심점)"""
    
    # 💡 엔티티의 핵심: 고유 식별자(Identity)
    id: int | None  # DB 저장 전에는 None일 수 있음
    
    # 💡 모든 속성은 원시 타입(str, int)이 아닌 도메인 VO로 구성
    passenger_id: PassengerId | None
    name: PassengerName
    gender: Gender
    age: Age
    family: FamilyRelations
    _survived: Literal["survived", "perished", "unknown"]  # 캡슐화를 위해 내부 상태로 관리

    @property
    def survived_status(self) -> str:
        return self._survived

    # 💡 안방마님 역할: 엔티티 내부에서 비즈니스 로직을 직접 수행 (Rich Domain Model)
    def record_survival_result(self, survived_code: int | None) -> None:
        """승객의 생존 결과를 도메인 규칙에 맞게 판별 및 기록"""
        if survived_code == 1:
            self._survived = "survived"
        elif survived_code == 0:
            self._survived = "perished"
        else:
            self._survived = "unknown"

    def is_vulnerable_demographic(self) -> bool:
        """비즈니스 로직: 구조 우선순위가 높은 취약 계층(여성 또는 아동)인지 판별"""
        is_child = self.age.value is not None and self.age.value < 16
        is_female = self.gender.value == "female"
        return is_child or is_female