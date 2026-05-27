from typing import Protocol

import pandas as pd

from titanic.app.schemas.titanic_schema import (
    TitanicDatasetSchemaResponse,
    TitanicModelMetricsResponse,
)


class TitanicQueryPort(Protocol):
    """타이타닉 조회 유스케이스 입력 포트."""

    def get_data(self) -> pd.DataFrame: ...

    def get_count(self) -> int: ...

    def get_survived_count(self) -> int: ...

    def get_dead_count(self) -> int: ...

    def has_decision_tree_model(self) -> bool: ...

    def get_dataset_schema(self) -> TitanicDatasetSchemaResponse: ...

    def get_model_name_and_accuracy(self) -> TitanicModelMetricsResponse: ...
