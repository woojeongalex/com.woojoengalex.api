from abc import ABC, abstractmethod

from the_wire.app.dtos.watch_dto import WatchStatusResult


class WatchRepositoryPort(ABC):
    @abstractmethod
    async def find_latest(self) -> WatchStatusResult | None: ...
