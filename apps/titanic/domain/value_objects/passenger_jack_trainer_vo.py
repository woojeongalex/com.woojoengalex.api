from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class GenderType(Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class PassengerId:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("빈 값")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class PassengerName:
    full_name: str

    def __post_init__(self):
        if not self.full_name or not self.full_name.strip():
            raise ValueError("빈 값")
        if len(self.full_name) > 200:
            raise ValueError("200자 초과")

    @property
    def normalized(self) -> str:
        return self.full_name.strip()


@dataclass(frozen=True)
class Gender:
    value: GenderType

    @classmethod
    def from_raw(cls, raw: str | None) -> Gender:
        if not raw:
            return cls(GenderType.UNKNOWN)
        normalized = raw.strip().lower()
        if normalized == "male":
            return cls(GenderType.MALE)
        if normalized == "female":
            return cls(GenderType.FEMALE)
        return cls(GenderType.UNKNOWN)

    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE


@dataclass(frozen=True)
class Age:
    value: float | None

    def __post_init__(self):
        if self.value is not None and (self.value < 0 or self.value > 120):
            raise ValueError("유효하지 않은 나이 범위")

    @classmethod
    def from_raw(cls, raw: str | None) -> Age:
        if not raw or not raw.strip():
            return cls(None)
        try:
            return cls(float(raw))
        except (ValueError, TypeError):
            raise ValueError("파싱 실패")

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def is_minor(self) -> bool:
        if self.value is None:
            return False
        return self.value < 18


@dataclass(frozen=True)
class FamilyRelation:
    sib_sp: int
    parch: int

    def __post_init__(self):
        if self.sib_sp < 0:
            raise ValueError("sib_sp는 음수 불가")
        if self.parch < 0:
            raise ValueError("parch는 음수 불가")

    @property
    def total_family_size(self) -> int:
        return self.sib_sp + self.parch

    @property
    def is_alone(self) -> bool:
        return self.total_family_size == 0

    @classmethod
    def from_raw(cls, sib_sp_raw, parch_raw) -> FamilyRelation:
        sib_sp = int(sib_sp_raw) if sib_sp_raw is not None else 0
        parch = int(parch_raw) if parch_raw is not None else 0
        return cls(sib_sp=sib_sp, parch=parch)


@dataclass(frozen=True)
class SurvivalStatus:
    survived: bool | None

    @classmethod
    def from_raw(cls, raw: str | None) -> SurvivalStatus:
        if not raw:
            return cls(None)
        if raw == "1":
            return cls(True)
        if raw == "0":
            return cls(False)
        raise ValueError("파싱 실패")

    @property
    def is_unknown(self) -> bool:
        return self.survived is None


# alias used by domain __init__.py
JackTrainerVo = SurvivalStatus
