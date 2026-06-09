from __future__ import annotations

from typing import Any

from titanic.app.dtos.crew_james_command import BookingCommand, PersonCommand
from titanic.app.ports.input.crew_james_use_case import JamesUseCase
from titanic.app.ports.output.crew_james_repository import JamesRepository


class JamesInteractor(JamesUseCase):
    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def introduce_myself(self) -> dict[str, Any]:
        return {
            "id": 1,
            "name": "James Cameron",
            "role": "감독 · 승객 데이터 업로드 담당",
            "description": (
                "타이타닉을 영화로 재현한 감독. "
                "승객 CSV 파일을 시스템에 업로드하고 데이터를 저장하는 일을 맡고 있습니다."
            ),
            "ability": "승객 CSV 파일 일괄 업로드",
            "notable_work": "Titanic (1997)",
        }

    async def upload(self, person_commands: list[PersonCommand], file_name: str) -> dict[str, Any]:
        '''CSV 파싱된 PersonCommand 리스트를 BookingCommand로 변환 후 저장'''
        booking_commands = [
            BookingCommand(
                pclass=cmd.pclass,
                ticket=cmd.ticket,
                fare=cmd.fare,
                cabin=cmd.cabin,
                embarked=cmd.embarked,
            )
            for cmd in person_commands
        ]
        count = await self._repository.upload(person_commands, booking_commands, file_name)
        return {"saved": count}