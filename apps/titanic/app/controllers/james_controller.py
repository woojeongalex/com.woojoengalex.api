import logging

import pandas as pd

from titanic.app.schemas.titanic_schema import TitanicDatasetSchemaResponse, TitanicModelMetricsResponse
from titanic.app.services.jack_service import JackService

logger = logging.getLogger(__name__)


class JamesController:
    """HTTP 진입점 — 비즈니스 로직은 JackService에 위임 (secom UserController 패턴)."""

    def __init__(self) -> None:
        self._service = JackService()

    def get_data(self) -> pd.DataFrame:
        logger.info("[TITANIC][james][2/controller] → service.get_data")
        return self._service.get_data()

    def get_count(self) -> int:
        return self._service.get_count()

    def get_survived_count(self) -> int:
        return self._service.get_survived_count()

    def get_dead_count(self) -> int:
        return self._service.get_dead_count()

    def has_decision_tree_model(self) -> bool:
        return self._service.has_decision_tree_model()

    def get_dataset_schema(self) -> TitanicDatasetSchemaResponse:
        return self._service.get_dataset_schema()

    def get_model_name_and_accuracy(self) -> TitanicModelMetricsResponse:
        logger.info("[TITANIC][james][2/controller] → service.get_model_name_and_accuracy")
        return self._service.get_model_name_and_accuracy()
