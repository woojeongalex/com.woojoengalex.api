from abc import ABC, abstractmethod

from vision.app.dtos.vision_dto import AnalyzeImageCommand, VisionResult


class VisionUseCase(ABC):
    @abstractmethod
    async def analyze(self, command: AnalyzeImageCommand) -> VisionResult: ...

    @abstractmethod
    async def list_results(self) -> list[VisionResult]: ...
