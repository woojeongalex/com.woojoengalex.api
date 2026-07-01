from fastapi import Depends
from the_wire.adapter.outbound.repositories.introduce_repository import (
    IntroduceRepository,
)
from the_wire.app.ports.input.introduce_use_case import IntroduceUseCase
from the_wire.app.ports.output.introduce_port import IntroducePort
from the_wire.app.use_cases.introduce_interactor import IntroduceInteractor


def get_introduce_repository() -> IntroducePort:
    return IntroduceRepository()


def get_introduce_use_case(
    repository: IntroducePort = Depends(get_introduce_repository),
) -> IntroduceUseCase:
    return IntroduceInteractor(repository=repository)
