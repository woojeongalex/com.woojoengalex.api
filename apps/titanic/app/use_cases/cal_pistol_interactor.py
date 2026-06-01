"""[Layer: Use Cases] Cal pistol (CalPistolUseCase 구현)."""

from titanic.app.ports.input.cal_pistol_use_case import CalPistolUseCase


class CalPistolInteractor(CalPistolUseCase):
    async def get_cal_pistol(self) -> None:
        pass
