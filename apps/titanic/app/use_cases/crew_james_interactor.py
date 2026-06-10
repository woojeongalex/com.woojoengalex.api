from __future__ import annotations

from typing import Any

from titanic.adapter.inbound.api.schemas.crew_james_introduce_schema import JamesIntroduceSchema
from titanic.app.dtos.crew_james_command import BookingCommand, JamesIntroduceResponse, JamesQuery, PersonCommand
from titanic.app.ports.input.crew_james_use_case import JamesUseCase
from titanic.app.ports.output.crew_james_repository import JamesRepository


class JamesInteractor(JamesUseCase):
    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: JamesIntroduceSchema) -> JamesIntroduceResponse:
        return await self._repository.introduce_myself(JamesQuery(
            id=schema.id,
            name=schema.name,
        ))

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