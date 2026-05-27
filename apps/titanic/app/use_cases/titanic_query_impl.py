import pandas as pd

from titanic.app.ports.input.titanic_query_port import TitanicQueryPort
from titanic.app.schemas.titanic_schema import (
    TitanicDatasetSchemaResponse,
    TitanicModelMetricsResponse,
)
from titanic.app.use_cases.train_use_case import TrainUseCase


class TitanicQueryImpl:
    """조회 유스케이스 — TrainUseCase에 위임."""

    def __init__(self, train: TrainUseCase | None = None) -> None:
        self._train = train or TrainUseCase()

    def get_data(self) -> pd.DataFrame:
        return self._train.get_data()

    def get_count(self) -> int:
        return self._train.get_count()

    def get_survived_count(self) -> int:
        return self._train.get_survived_count()

    def get_dead_count(self) -> int:
        return self._train.get_dead_count()

    def has_decision_tree_model(self) -> bool:
        return self._train.has_decision_tree_model()

    def get_dataset_schema(self) -> TitanicDatasetSchemaResponse:
        return self._train.get_dataset_schema()

    def get_model_name_and_accuracy(self) -> TitanicModelMetricsResponse:
        return self._train.get_model_name_and_accuracy()


def get_titanic_query() -> TitanicQueryPort:
    return TitanicQueryImpl()
