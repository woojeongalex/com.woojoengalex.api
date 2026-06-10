from abc import ABC, abstractmethod

from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse


class SmithCaptainRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        pass
