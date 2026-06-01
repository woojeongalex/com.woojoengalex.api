"""[Layer: Use Cases] Andrews blueprint (AndrewsBlueprintUseCase 구현)."""

from titanic.app.ports.input.andrews_blueprint_use_case import AndrewsBlueprintUseCase


class AndrewsBlueprintInteractor(AndrewsBlueprintUseCase):
    async def get_andrews_blueprint(self) -> None:
        pass
