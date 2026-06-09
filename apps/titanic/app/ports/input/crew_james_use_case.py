from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.crew_james_command import PersonCommand


class JamesUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self) -> dict[str, Any]:
        pass

    @abstractmethod
    async def upload(self, person_commands: list[PersonCommand], file_name: str) -> dict[str, Any]:
        '''제임스 감독의 CSV 파일 업로드 메소드'''
        pass
