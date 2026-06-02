"""[Layer: Ports] James 입력 Port — upload (inbound → usecase)."""

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.james_dto import PersonCommand


class JamesUseCase(ABC):
    @abstractmethod
    async def receive_uploaded_records(
        self, person_commands: list[PersonCommand], file_name: str
    ) -> dict[str, Any]:
        pass
