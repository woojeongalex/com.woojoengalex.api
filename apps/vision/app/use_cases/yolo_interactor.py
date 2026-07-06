import logging

from ultralytics import YOLO
from vision.app.dtos.train_face_dto import TrainFaceCommand, TrainFaceResult
from vision.app.ports.input.train_face_use_case import TrainFaceUseCase
from vision.app.ports.output.yolo_port import YoloPort

logger = logging.getLogger(__name__)

_BASE_MODEL = "yolo11n.pt"


class YoloInteractor(TrainFaceUseCase):
    def __init__(self, dataset_port: YoloPort) -> None:
        self.dataset_port = dataset_port

    def train(self, command: TrainFaceCommand) -> TrainFaceResult:
        dataset_yaml = self.dataset_port.get_dataset_config_path()
        logger.info(
            "[YoloInteractor] train | dataset=%s epochs=%d",
            dataset_yaml,
            command.epochs,
        )

        model = YOLO(_BASE_MODEL)
        results = model.train(
            data=dataset_yaml,
            epochs=command.epochs,
            batch=command.batch_size,
            imgsz=command.image_size,
        )
        weights_path = str(results.save_dir / "weights" / "best.pt")
        logger.info("[YoloInteractor] 학습 완료 weights_path=%s", weights_path)
        return TrainFaceResult(
            weights_path=weights_path, epochs_completed=command.epochs
        )
