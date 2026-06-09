from abc import ABC, abstractmethod
from typing import Any


class SmithCaptainRepository(ABC):
    @abstractmethod
    async def get_smith_captain(self) -> dict[str, Any]:
        pass
