from dataclasses import dataclass


@dataclass(frozen=True)
class TrainFaceCommand:
    epochs: int = 50
    batch_size: int = 16
    image_size: int = 224


@dataclass(frozen=True)
class TrainFaceResult:
    weights_path: str
    epochs_completed: int
