from abc import ABC, abstractmethod

import numpy as np
from the_wire.app.dtos.inbox_dto import InboxResult, ReceiveMailCommand


class InboxRepositoryPort(ABC):
    @abstractmethod
    async def save(
        self, command: ReceiveMailCommand, embedding: np.ndarray | None = None
    ) -> InboxResult: ...

    @abstractmethod
    async def find_all(self) -> list[InboxResult]: ...
