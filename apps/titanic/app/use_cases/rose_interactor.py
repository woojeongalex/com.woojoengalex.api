"""[Layer: Use Cases] Rose — 데이터셋 스키마 (RoseUseCase 구현)."""

from titanic.app.ports.input.rose_use_case import RoseUseCase


class RoseInteractor(RoseUseCase):
    def read_titanic_schema(self) -> None:
        pass
