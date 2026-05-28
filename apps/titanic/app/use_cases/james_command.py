from titanic.adapter.inbound.api.schemas.titanic_request import TitanicCommandRequest


class JamesCommand:
    """업로드된 Titanic command rows를 애플리케이션 계층에서 처리."""

    def move_uploaded_rows(
        self,
        file_name: str,
        rows: list[TitanicCommandRequest],
    ) -> dict[str, object]:
        return {
            "file_name": file_name,
            "count": len(rows),
            "rows": [row.model_dump(by_alias=False) for row in rows],
        }

