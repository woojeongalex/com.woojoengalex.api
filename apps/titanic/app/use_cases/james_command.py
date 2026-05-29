"""[Layer: Use Cases] James — upload 업무 오케스트레이션."""

from abc import ABC, abstractmethod
from dataclasses import asdict
from typing import Any

from titanic.app.dtos.passenger_row import PassengerRowDto
from titanic.app.dtos.upload_result import UploadResultDto
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.output.james_repository_port import JamesRepositoryPort
from titanic.app.titanic_flow_log import titanic_flow_log


class JamesCommand(ABC):
    @abstractmethod
    async def receive_uploaded_records(records: list[dict[str, Any]]) -> None:
        pass


class JamesCommandImpl(JamesCommand, JamesUseCase):
    repository: type[JamesRepositoryPort]

    @staticmethod
    async def receive_uploaded_records(records: list[dict[str, Any]]) -> None:
        if not records:
            return
        file_name = str(records[0].get("source_file", "upload.csv"))
        passengers = [PassengerRowDto(**row) for row in records]
        await JamesCommandImpl.save_upload(file_name, passengers)

    @staticmethod
    async def save_upload(
        file_name: str,
        passengers: list[PassengerRowDto],
    ) -> UploadResultDto:
        titanic_flow_log(
            "james-upload",
            "usecase",
            "save_upload passengers=%s",
            len(passengers),
            source_file=file_name,
        )
        records = [asdict(passenger) for passenger in passengers]
        result = await JamesCommandImpl.repository.save_upload(file_name, records)
        return UploadResultDto(
            file_name=str(result["file_name"]),
            count=int(result["count"]),
        )
