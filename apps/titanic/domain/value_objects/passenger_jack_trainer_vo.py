from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class PassengerId:
    """승객 고유 식별 번호 VO (자체 검증 로직 포함)"""
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("승객 ID는 음수일 수 없습니다.")


@dataclass(frozen=True)
class PassengerName:
    """승객 이름 VO"""
    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("승객 이름은 비어있을 수 없습니다.")


@dataclass(frozen=True)
class Gender:
    """성별 VO (정해진 도메인 값만 허용)"""
    value: Literal["male", "female", "unknown"]

    @classmethod
    def from_str(cls, val: str | None) -> "Gender":
        if not val:
            return cls("unknown")
        clean_val = val.strip().lower()
        if clean_val in ["male", "female"]:
            return cls(clean_val)
        return cls("unknown")


@dataclass(frozen=True)
class Age:
    """나이 VO (결측치 및 도메인 범위 검증)"""
    value: float | None

    def __post_init__(self):
        if self.value is not None and (self.value < 0 or self.value > 120):
            raise ValueError("유효하지 않은 나이 범위입니다.")

    @property
    def is_missing(self) -> bool:
        return self.value is None


@dataclass(frozen=True)
class FamilyRelations:
    """가족 관계 VO (형제/배우자 수와 부모/자녀 수를 결합한 개념)"""
    sib_sp: int  # 형제 자매 / 배우자 수
    parch: int   # 부모 / 자녀 수

    def __post_init__(self):
        if self.sib_sp < 0 or self.parch < 0:
            raise ValueError("가족 구성원 수는 음수일 수 없습니다.")

    @property
    def total_family_size(self) -> int:
        """비즈니스 로직: 동반한 총 가족 수 계산"""
        return self.sib_sp + self.parch
    
    @property
    def Is_alone(self) -> bool:
        """비즈니스 로직: 홀로 탑승했는지 여부"""
        return self.total_family_size == 0