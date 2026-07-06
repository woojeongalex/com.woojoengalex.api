from abc import ABC, abstractmethod

from vision.app.dtos.vision_dto import VisionResult


class VisionRepositoryPort(ABC):
    @abstractmethod
    async def save(
        self, file_name: str, label: str, confidence: float
    ) -> VisionResult: ...

    @abstractmethod
    async def find_all(self) -> list[VisionResult]: ...
