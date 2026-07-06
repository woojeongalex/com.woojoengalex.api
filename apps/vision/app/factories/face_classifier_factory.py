import os

import numpy as np
from ultralytics import YOLO

_MODEL_PATH = os.getenv(
    "VISION_FACE_MODEL_PATH",
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "resources",
        "weights",
        "face_classifier.pt",
    ),
)
_model_cache: YOLO | None = None


def get_face_classifier() -> YOLO:
    global _model_cache
    if _model_cache is None:
        _model_cache = YOLO(_MODEL_PATH)
    return _model_cache


def classify_face(image: np.ndarray) -> tuple[str, float]:
    model = get_face_classifier()
    result = model(image, verbose=False)[0]
    label = result.names[result.probs.top1]
    confidence = float(result.probs.top1conf)
    return label, confidence
