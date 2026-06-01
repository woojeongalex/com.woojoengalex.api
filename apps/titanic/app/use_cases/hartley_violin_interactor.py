"""[Layer: Use Cases] Hartley violin (HartleyViolinUseCase 구현)."""

from titanic.app.ports.input.hartley_violin_use_case import HartleyViolinUseCase


class HartleyViolinInteractor(HartleyViolinUseCase):
    async def get_hartley_violin(self) -> None:
        pass
