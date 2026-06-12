from __future__ import annotations

from titanic.app.dtos.crew_james_director_dto import (
    BookingCommand,
    JamesDirectorQuery,
    JamesDirectorResponse,
    PersonCommand,
)


class JamesDirectorInteractor:
    def __init__(self, repository) -> None:
        self._repository = repository

    async def introduce_myself(self, request) -> JamesDirectorResponse:
        return await self._repository.introduce_myself(JamesDirectorQuery(
            id=request.id,
            name=request.name,
        ))

    async def upload_titanic_file(self, rows: list) -> dict:
        person_commands = [
            PersonCommand(
                passenger_id=row.passenger_id or "",
                survived=row.survived if row.survived is not None else "",
                name=row.name or "",
                gender=row.gender or "",
                age=row.age or "",
                sib_sp=row.sib_sp or "",
                parch=row.parch or "",
            )
            for row in rows
        ]
        booking_commands = [
            BookingCommand(
                pclass=row.pclass or "",
                ticket=row.ticket or "",
                fare=row.fare or "",
                cabin=row.cabin if row.cabin is not None else "",
                embarked=row.embarked or "",
            )
            for row in rows
        ]
        count = await self._repository.receive_uploaded_records(person_commands, booking_commands)
        return {"saved": count}
