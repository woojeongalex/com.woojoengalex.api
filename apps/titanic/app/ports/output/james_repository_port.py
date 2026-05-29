"""[Layer: Ports] James 출력 Port — upload 저장 계약."""

from abc import ABC, abstractmethod
from typing import Any


class JamesRepositoryPort(ABC):
    @abstractmethod
    async def save_upload(
        file_name: str, records: list[dict[str, Any]]
    ) -> dict[str, Any]:
        pass
