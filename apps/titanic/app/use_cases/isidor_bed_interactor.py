"""[Layer: Use Cases] Isidor bed (IsidorBedUseCase 구현)."""

from titanic.app.ports.input.isidor_bed_use_case import IsidorBedUseCase


class IsidorBedInteractor(IsidorBedUseCase):
    async def get_isidor_bed(self) -> None:
        pass
