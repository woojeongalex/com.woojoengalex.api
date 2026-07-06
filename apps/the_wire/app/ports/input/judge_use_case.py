from abc import ABC, abstractmethod

from the_wire.app.dtos.introduce_dto import IntroduceQuery, IntroduceResponse
from the_wire.app.dtos.judge_dto import JudgeCommand, JudgeResult


class JudgeUseCase(ABC):
    @abstractmethod
    def judge(self, command: JudgeCommand) -> JudgeResult: ...

    @abstractmethod
    async def introduce_myself(self, query: IntroduceQuery) -> IntroduceResponse: ...
