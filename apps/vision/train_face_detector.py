import logging

from vision.app.dtos.train_face_dto import TrainFaceCommand
from vision.dependencies.train_face_provider import get_train_face_use_case

logger = logging.getLogger(__name__)


def run_training_pipeline(epochs: int = 50, batch_size: int = 16) -> None:
    trainer = get_train_face_use_case()
    logger.info(
        "[train_face_detector] 얼굴 인식 파인튜닝 시작 epochs=%d batch_size=%d",
        epochs,
        batch_size,
    )
    result = trainer.train(TrainFaceCommand(epochs=epochs, batch_size=batch_size))
    logger.info("[train_face_detector] 학습 완료 weights_path=%s", result.weights_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_training_pipeline()
