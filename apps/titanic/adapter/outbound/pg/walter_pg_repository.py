"""[Layer: Outbound] Walter PG — 승객 조회 (person + booking)."""

import logging
from math import ceil

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from titanic.adapter.outbound.orm.booking_orm import BookingOrm
from titanic.adapter.outbound.orm.person_orm import PersonOrm
from titanic.app.dtos.walter_page import WalterPassengerPageDto
from titanic.app.ports.output.walter_repository_port import WalterRepositoryPort

logger = logging.getLogger(__name__)


class WalterPgRepository(WalterRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageDto:
        base = select(PersonOrm, BookingOrm).join(
            BookingOrm, BookingOrm.person_id == PersonOrm.id
        )
        count_stmt = (
            select(func.count())
            .select_from(PersonOrm)
            .join(BookingOrm, BookingOrm.person_id == PersonOrm.id)
        )
        if source_file:
            base = base.where(PersonOrm.source_file == source_file)
            count_stmt = count_stmt.where(PersonOrm.source_file == source_file)

        total = (await self._session.execute(count_stmt)).scalar_one()
        result = await self._session.execute(
            base.order_by(PersonOrm.id)
            .offset((page - 1) * size)
            .limit(size)
        )
        pairs = result.all()

        rows = [
            {
                "id": person.id,
                "source_file": person.source_file,
                "passenger_id": person.passenger_id,
                "survived": person.survived,
                "pclass": booking.pclass,
                "name": person.name,
                "gender": person.gender,
                "age": person.age,
                "sib_sp": person.sib_sp,
                "parch": person.parch,
                "ticket": booking.ticket,
                "fare": booking.fare,
                "created_at": person.created_at.isoformat() if person.created_at else None,
            }
            for person, booking in pairs
        ]
        logger.info("###############################################")
        logger.info("💊[월터 레포지터리] Neon 조회")
        logger.info(f"👍🏻total: {total}")
        logger.info(f"🐥page: {page}")
        logger.info(f"🦜상위 5개: {rows[:5]}")
        logger.info("###############################################")

        return WalterPassengerPageDto(
            source_file=source_file,
            page=page,
            size=size,
            total=total,
            total_pages=ceil(total / size) if total else 0,
            rows=rows,
        )
