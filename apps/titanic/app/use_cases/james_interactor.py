"""[Layer: Use Cases] James — upload 업무 오케스트레이션 (JamesUseCase 구현)."""

from typing import Any

from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.output.james_repository_port import JamesRepositoryPort


class JamesInteractor(JamesUseCase):
    repository: type[JamesRepositoryPort]

    @classmethod
    async def receive_uploaded_records(
        cls, records: list[dict[str, Any]], file_name: str
    ) -> dict[str, Any]:
        return await cls.repository.save_upload(file_name, records)
