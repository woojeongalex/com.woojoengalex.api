from abc import ABC, abstractmethod

from titanic.app.dtos.crew_james_command import BookingCommand, PersonCommand


class JamesRepository(ABC):
    @abstractmethod
    async def upload(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
        file_name: str,
    ) -> int:
        pass
