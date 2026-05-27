"""승객·학습용 행 검증 (Survived, Sex, Embarked 등)."""

from typing import Any

import pandas as pd

from titanic.app.schemas.dataset_columns import ML_FEATURE_COLUMNS, ML_TARGET_COLUMN

_VALID_SURVIVED = {0, 1}
_VALID_SEX = {"male", "female"}
_VALID_EMBARKED = {"C", "Q", "S"}


class ValidationUseCase:
    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_survived(value: Any) -> bool:
        try:
            return int(value) in _VALID_SURVIVED
        except (TypeError, ValueError):
            return False

    @staticmethod
    def validate_sex(value: Any) -> bool:
        return isinstance(value, str) and value in _VALID_SEX

    @staticmethod
    def validate_embarked(value: Any) -> bool:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return True
        return isinstance(value, str) and value in _VALID_EMBARKED

    @staticmethod
    def validate_training_frame(df: pd.DataFrame) -> None:
        """학습용 DataFrame에 필수 컬럼·값域이 있는지 확인."""
        required = set(ML_FEATURE_COLUMNS) | {ML_TARGET_COLUMN}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"학습 데이터에 필수 컬럼이 없습니다: {sorted(missing)}")

        if not df[ML_TARGET_COLUMN].apply(ValidationUseCase.validate_survived).all():
            raise ValueError(f"{ML_TARGET_COLUMN} 값은 0 또는 1이어야 합니다.")

        if "Sex" in df.columns and not df["Sex"].apply(ValidationUseCase.validate_sex).all():
            raise ValueError("Sex 값은 male 또는 female이어야 합니다.")
