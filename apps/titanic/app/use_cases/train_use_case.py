import logging

import pandas as pd
from sklearn.model_selection import train_test_split

from titanic.app.use_cases.rose_query import RoseQuery
from titanic.adapter.inbound.api.schemas.dataset_columns import (
    EXTRA_CSV_COLUMNS,
    ML_FEATURE_COLUMNS,
    ML_TARGET_COLUMN,
    TITANIC_COLUMN_SPECS,
)
from titanic.adapter.inbound.api.schemas.titanic_schema import (
    TitanicColumnInfo,
    TitanicDatasetSchemaResponse,
    TitanicModelMetricsResponse,
)
from titanic.app.use_cases.validation_use_case import ValidationUseCase
from titanic.app.use_cases.walter_query import WalterUseCase

logger = logging.getLogger(__name__)


class TrainUseCase:
    _RANDOM_STATE = 42
    _accuracy: float | None = None
    _model_name: str | None = None

    def __init__(self) -> None:
        self._reader = WalterUseCase()
        self._rose_query = RoseQuery()
        self._validation = ValidationUseCase()

    def get_data(self) -> pd.DataFrame:
        return self._reader.get_sample_row()

    def get_count(self) -> int:
        return self._reader.get_passenger_count()

    def get_survived_count(self) -> int:
        return self._reader.get_survived_count()

    def get_dead_count(self) -> int:
        return self._reader.get_dead_count()

    def has_decision_tree_model(self) -> bool:
        return self._rose_query.model is not None

    def get_dataset_schema(self) -> TitanicDatasetSchemaResponse:
        specs = TITANIC_COLUMN_SPECS + EXTRA_CSV_COLUMNS
        return TitanicDatasetSchemaResponse(
            columns=[TitanicColumnInfo(**s) for s in specs],
            ml_features=list(ML_FEATURE_COLUMNS),
            ml_target=ML_TARGET_COLUMN,
        )

    def get_model_name_and_accuracy(self) -> TitanicModelMetricsResponse:
        if TrainUseCase._accuracy is None:
            df = self._reader.get_full_data()
            df = df[list(ML_FEATURE_COLUMNS) + [ML_TARGET_COLUMN]].copy()
            self._validation.validate_training_frame(df)

            df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
            df["Age"] = df["Age"].fillna(df["Age"].median())
            df["Fare"] = df["Fare"].fillna(df["Fare"].median())

            X = df[list(ML_FEATURE_COLUMNS)]
            y = df[ML_TARGET_COLUMN]
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=self._RANDOM_STATE,
            )
            self._rose_query.model.fit(X_train, y_train)

            TrainUseCase._accuracy = float(self._rose_query.model.score(X_test, y_test))
            TrainUseCase._model_name = self._rose_query.get_model_name()
            logger.info(
                "[TITANIC][train][use_case] 모델 학습 완료 name=%s accuracy=%.4f",
                TrainUseCase._model_name,
                TrainUseCase._accuracy,
            )

        return TitanicModelMetricsResponse(
            model_name=TrainUseCase._model_name or "",
            accuracy=TrainUseCase._accuracy or 0.0,
        )
