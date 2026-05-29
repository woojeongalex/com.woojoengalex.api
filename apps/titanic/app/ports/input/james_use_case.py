"""[Layer: Ports] James 입력 Port — upload 만 (inbound → usecase)."""

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_row import PassengerRowDto
from titanic.app.dtos.upload_result import UploadResultDto


class JamesUseCase(ABC):
    @abstractmethod
    async def save_upload(
        file_name: str,
        passengers: list[PassengerRowDto],
    ) -> UploadResultDto:
        pass
