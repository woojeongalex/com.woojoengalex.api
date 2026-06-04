"""[Layer: Use Cases] James — upload 업무 오케스트레이션 (JamesUseCase 구현)."""

import logging
from dataclasses import asdict
from typing import Any

from titanic.app.dtos.james_command import BookingCommand, PersonCommand
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.output.james_repository_port import JamesRepositoryPort

logger = logging.getLogger(__name__)

class JamesInteractor(JamesUseCase):
    repository: type[JamesRepositoryPort]

    @classmethod
    async def receive_uploaded_records(
        cls, person_commands: list[PersonCommand], file_name: str
    ) -> dict[str, Any]:
        booking_commands: list[BookingCommand] = [
            BookingCommand(
                pclass=person.pclass,
                ticket=person.ticket,
                fare=person.fare,
                cabin=person.cabin,
                embarked=person.embarked,
            )
            for person in person_commands
        ]

        logger.info(
            "[제임스 유스케이스] 라우터에서 유스케이스로 옮겨진 스키마 상위 5개 레코드: %s",
            [asdict(person) for person in person_commands[:5]],
        )

        count = await cls.repository.receive_uploaded_records(
            person_commands,
            booking_commands,
            file_name,
        )
        return {"file_name": file_name, "count": count}