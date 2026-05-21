import logging

import pandas as pd
from sklearn.model_selection import train_test_split

from titanic.app.models.rose_model import RoseModel
from titanic.app.repositories.walter_repository import WalterRepository
from titanic.app.schemas.dataset_columns import (
    EXTRA_CSV_COLUMNS,
    ML_FEATURE_COLUMNS,
    ML_TARGET_COLUMN,
    TITANIC_COLUMN_SPECS,
)
from titanic.app.schemas.titanic_schema import (
    TitanicColumnInfo,
    TitanicDatasetSchemaResponse,
    TitanicModelMetricsResponse,
)
from titanic.app.validators.caledon_validation import CaledonValidation

logger = logging.getLogger(__name__)


class JackService:
    _RANDOM_STATE = 42
    _accuracy: float | None = None
    _model_name: str | None = None

    def __init__(self) -> None:
        self._repository = WalterRepository()
        self._rose = RoseModel()
        self._validation = CaledonValidation()

    def get_data(self) -> pd.DataFrame:
        return self._repository.get_sample_row()

    def get_count(self) -> int:
        return self._repository.get_passenger_count()

    def get_survived_count(self) -> int:
        return self._repository.get_survived_count()

    def get_dead_count(self) -> int:
        return self._repository.get_dead_count()

    def has_decision_tree_model(self) -> bool:
        return self._rose.model is not None

    def get_dataset_schema(self) -> TitanicDatasetSchemaResponse:
        specs = TITANIC_COLUMN_SPECS + EXTRA_CSV_COLUMNS
        return TitanicDatasetSchemaResponse(
            columns=[TitanicColumnInfo(**s) for s in specs],
            ml_features=list(ML_FEATURE_COLUMNS),
            ml_target=ML_TARGET_COLUMN,
        )

    def get_model_name_and_accuracy(self) -> TitanicModelMetricsResponse:
        if JackService._accuracy is None:
            df = self._repository.get_full_data()
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
            self._rose.model.fit(X_train, y_train)

            JackService._accuracy = float(self._rose.model.score(X_test, y_test))
            JackService._model_name = self._rose.get_model_name()
            logger.info(
                "[TITANIC][jack][4/service] 모델 학습 완료 name=%s accuracy=%.4f",
                JackService._model_name,
                JackService._accuracy,
            )

        return TitanicModelMetricsResponse(
            model_name=JackService._model_name or "",
            accuracy=JackService._accuracy or 0.0,
        )
