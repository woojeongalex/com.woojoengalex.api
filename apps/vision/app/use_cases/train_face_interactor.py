import logging

from ultralytics import YOLO
from vision.app.dtos.train_face_dto import TrainFaceCommand, TrainFaceResult
from vision.app.ports.input.train_face_use_case import TrainFaceUseCase
from vision.app.ports.output.face_dataset_port import FaceDatasetPort

logger = logging.getLogger(__name__)

_BASE_MODEL = "yolov8n-cls.pt"


class TrainFaceInteractor(TrainFaceUseCase):
    def __init__(self, dataset_port: FaceDatasetPort) -> None:
        self.dataset_port = dataset_port

    def train(self, command: TrainFaceCommand) -> TrainFaceResult:
        dataset_dir = self.dataset_port.get_dataset_config_path()
        logger.info(
            "[TrainFaceInteractor] train | dataset=%s epochs=%d",
            dataset_dir,
            command.epochs,
        )

        model = YOLO(_BASE_MODEL)
        results = model.train(
            data=dataset_dir,
            epochs=command.epochs,
            batch=command.batch_size,
            imgsz=command.image_size,
            workers=0,
        )
        weights_path = str(results.save_dir / "weights" / "best.pt")
        logger.info("[TrainFaceInteractor] 학습 완료 weights_path=%s", weights_path)
        return TrainFaceResult(
            weights_path=weights_path, epochs_completed=command.epochs
        )
