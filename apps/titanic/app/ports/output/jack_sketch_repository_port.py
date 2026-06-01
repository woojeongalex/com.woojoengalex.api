"""[Layer: Ports] Jack sketch 출력 Port — 조회 계약."""

from abc import ABC, abstractmethod
from typing import Any


class JackSketchRepositoryPort(ABC):
    @abstractmethod
    async def get_jack_sketch(self) -> dict[str, Any]:
        pass
