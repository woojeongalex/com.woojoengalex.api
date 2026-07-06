import os

from vision.adapter.outbound.repositories.face_dataset_local_repository import (
    FaceDatasetLocalRepository,
)
from vision.app.ports.input.train_face_use_case import TrainFaceUseCase
from vision.app.ports.output.face_dataset_port import FaceDatasetPort
from vision.app.use_cases.train_face_interactor import TrainFaceInteractor

_DEFAULT_DATASET_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "resources", "yolo_train"
)


def get_face_dataset_repository(
    base_path: str = _DEFAULT_DATASET_PATH,
) -> FaceDatasetPort:
    return FaceDatasetLocalRepository(base_path=base_path)


def get_train_face_use_case() -> TrainFaceUseCase:
    return TrainFaceInteractor(dataset_port=get_face_dataset_repository())
