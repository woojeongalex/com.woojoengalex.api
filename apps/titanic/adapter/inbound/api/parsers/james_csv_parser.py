"""James upload CSV → `JamesSchema` 목록."""

import csv
import io

from pydantic import ValidationError

from titanic.adapter.inbound.api.schemas.james_schema import (
    JAMES_CSV_COLUMNS,
    JamesSchema,
    has_james_csv_column,
)


class JamesCsvError(ValueError):
    pass


def parse_james_csv(text: str) -> list[JamesSchema]:
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise JamesCsvError("CSV 헤더가 없습니다.")

    fieldnames = list(reader.fieldnames)
    missing = [
        col for col in JAMES_CSV_COLUMNS if not has_james_csv_column(col, fieldnames)
    ]
    if missing:
        raise JamesCsvError(f"필수 컬럼이 없습니다: {', '.join(missing)}")

    records = list(reader)
    if not records:
        raise JamesCsvError("CSV에 데이터 행이 없습니다.")

    try:
        return [JamesSchema.model_validate(row) for row in records]
    except ValidationError:
        raise
