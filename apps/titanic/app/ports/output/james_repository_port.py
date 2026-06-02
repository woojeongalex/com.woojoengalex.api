"""[Layer: Ports] James 출력 Port — Person/Booking 저장 계약."""

from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.james_dto import BookingCommand, PersonCommand


class JamesRepositoryPort(ABC):
    @abstractmethod
    async def receive_uploaded_records(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        pass
