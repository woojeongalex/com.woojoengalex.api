from abc import ABC, abstractmethod

from the_wire.app.dtos.judge_dto import JudgeResult


class JudgeRepositoryPort(ABC):
    @abstractmethod
    async def save(self, result: JudgeResult) -> JudgeResult: ...

    @abstractmethod
    async def find_all(self) -> list[JudgeResult]: ...
