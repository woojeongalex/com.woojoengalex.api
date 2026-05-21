from pathlib import Path

import pandas as pd

_CSV_PATH = Path(__file__).resolve().parent.parent / "Titanic-Dataset.csv"


class WalterRepository:
    """타이타닉 CSV 데이터 접근 (secom Repository 레이어와 동일 역할)."""

    def __init__(self) -> None:
        pass

    def _read_csv(self) -> pd.DataFrame:
        return pd.read_csv(_CSV_PATH)

    def get_sample_row(self) -> pd.DataFrame:
        df = self._read_csv()
        return df.iloc[[0]].astype(object).where(df.iloc[[0]].notna(), None)

    def get_passenger_count(self) -> int:
        return int(self._read_csv().shape[0])

    def get_survived_count(self) -> int:
        df = self._read_csv()
        return int((df["Survived"] == 1).sum())

    def get_dead_count(self) -> int:
        df = self._read_csv()
        return int((df["Survived"] == 0).sum())

    def get_full_data(self) -> pd.DataFrame:
        return self._read_csv()
