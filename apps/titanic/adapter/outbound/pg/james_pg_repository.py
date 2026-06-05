import logging

from dataclasses import asdict

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from titanic.adapter.outbound.orm.booking_orm import BookingOrm
from titanic.adapter.outbound.orm.person_orm import PersonOrm
from titanic.app.dtos.james_command import BookingCommand, PersonCommand
from titanic.app.ports.output.james_repository_port import JamesRepositoryPort
from titanic.app.titanic_flow_log import titanic_flow_log

logger = logging.getLogger(__name__)


class JamesPgRepository(JamesRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upload(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
        file_name: str,
    ) -> int:
        logger.info(
            "[제임스 레포지터리] PersonCommand 상위 5개 레코드: %s",
            [asdict(person) for person in person_commands[:5]],
        )
        logger.info(
            "[제임스 레포지터리] BookingCommand 상위 5개 레코드: %s",
            [asdict(booking) for booking in booking_commands[:5]],
        )

        person_ids = (
            await self._session.execute(
                select(PersonOrm.id).where(PersonOrm.source_file == file_name)
            )
        ).scalars().all()
        if person_ids:
            await self._session.execute(
                delete(BookingOrm).where(BookingOrm.person_id.in_(person_ids))
            )
        await self._session.execute(
            delete(PersonOrm).where(PersonOrm.source_file == file_name)
        )

        persons = [
            PersonOrm.from_command(file_name, person) for person in person_commands
        ]
        self._session.add_all(persons)
        await self._session.flush()

        bookings = [
            BookingOrm.from_command(person.id, booking)
            for person, booking in zip(persons, booking_commands, strict=True)
        ]
        self._session.add_all(bookings)

        logger.info(
            "[제임스 레포지터리] 저장 시작 file=%s rows=%s",
            file_name,
            len(persons),
        )
        titanic_flow_log(
            "james-upload",
            "outbound",
            "Neon person/booking rows=%s",
            len(persons),
            source_file=file_name,
        )
        await self._session.commit()
        logger.info(
            "[제임스 레포지터리] 저장 완료 file=%s rows=%s",
            file_name,
            len(persons),
        )
        return len(persons)
