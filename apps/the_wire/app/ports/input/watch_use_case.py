from abc import ABC, abstractmethod

from the_wire.app.dtos.watch_dto import (
    PolicyFilterCommand,
    PolicyFilterResult,
    WatchStatusResult,
)


class WatchUseCase(ABC):
    @abstractmethod
    async def read_status(self) -> WatchStatusResult | None: ...

    @abstractmethod
    def filter(self, command: PolicyFilterCommand) -> PolicyFilterResult: ...
