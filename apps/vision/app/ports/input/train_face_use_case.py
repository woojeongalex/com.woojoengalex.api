from abc import ABC, abstractmethod

from vision.app.dtos.train_face_dto import TrainFaceCommand, TrainFaceResult


class TrainFaceUseCase(ABC):
    @abstractmethod
    def train(self, command: TrainFaceCommand) -> TrainFaceResult: ...
