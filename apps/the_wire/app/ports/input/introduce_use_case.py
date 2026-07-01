from abc import ABC, abstractmethod

from the_wire.app.dtos.introduce_dto import IntroduceQuery, IntroduceResponse


class IntroduceUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, query: IntroduceQuery) -> IntroduceResponse: ...
