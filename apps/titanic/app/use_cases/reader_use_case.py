class ReaderUseCase:
    """(DEPRECATED) 프로젝트 내부 파일(CSV) 읽기 제거됨.

    업로드/DB 기반으로 전환되기 전까지는 사용하지 않는다.
    """

    def _disabled(self) -> None:
        raise RuntimeError(
            "프로젝트 내부 CSV 파일 읽기 기능이 제거되었습니다. 업로드/DB 기반으로만 제공됩니다."
        )

    def get_sample_row(self):
        self._disabled()

    def get_passenger_count(self) -> int:
        self._disabled()
        return 0

    def get_survived_count(self) -> int:
        self._disabled()
        return 0

    def get_dead_count(self) -> int:
        self._disabled()
        return 0

    def get_full_data(self):
        self._disabled()
