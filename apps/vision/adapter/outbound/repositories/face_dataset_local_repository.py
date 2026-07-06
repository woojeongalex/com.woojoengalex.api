import os

from vision.app.ports.output.face_dataset_port import FaceDatasetPort


class FaceDatasetLocalRepository(FaceDatasetPort):
    def __init__(self, base_path: str) -> None:
        self.base_path = base_path

    def get_dataset_config_path(self) -> str:
        train_dir = os.path.join(self.base_path, "train")
        val_dir = os.path.join(self.base_path, "val")
        if not os.path.isdir(train_dir) or not os.path.isdir(val_dir):
            raise FileNotFoundError(
                f"YOLO 분류용 train/val 폴더를 찾을 수 없음: {train_dir}, {val_dir}"
            )
        return self.base_path
