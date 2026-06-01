"""[Layer: Ports] James 입력 Port — upload (inbound → usecase)."""

from abc import ABC, abstractmethod
from typing import Any


class JamesUseCase(ABC):
    @abstractmethod
    async def receive_uploaded_records(
        self, records: list[dict[str, Any]], file_name: str
    ) -> dict[str, Any]:
        pass
