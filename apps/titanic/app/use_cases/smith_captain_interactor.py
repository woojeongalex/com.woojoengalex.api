"""[Layer: Use Cases] Smith captain (SmithCaptainUseCase 구현)."""

from titanic.app.ports.input.smith_captain_use_case import SmithCaptainUseCase


class SmithCaptainInteractor(SmithCaptainUseCase):
    async def get_smith_captain(self) -> None:
        pass
