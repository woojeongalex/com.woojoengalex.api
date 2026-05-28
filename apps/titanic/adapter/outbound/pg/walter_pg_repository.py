from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from titanic.adapter.inbound.api.schemas.titanic_schema import (
    WalterPassengerItem,
    WalterPassengerPageResponse,
)
from titanic.adapter.outbound.orm.titanic_passenger_orm import TitanicPassengerOrm
from titanic.app.titanic_flow_log import titanic_flow_log


class WalterPgRepository:
    """PG 어댑터 — 타이타닉 승객 목록 조회."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def read_passengers(
        self,
        source_file: str | None,
        page: int,
        size: int,
    ) -> WalterPassengerPageResponse:
        normalized_page = max(1, page)
        normalized_size = max(1, min(size, 100))

        selected_source = source_file
        if not selected_source:
            latest_stmt = (
                select(TitanicPassengerOrm.source_file)
                .order_by(TitanicPassengerOrm.id.desc())
                .limit(1)
            )
            selected_source = await self._db.scalar(latest_stmt)

        if not selected_source:
            return WalterPassengerPageResponse(
                source_file=None,
                page=normalized_page,
                size=normalized_size,
                total=0,
                total_pages=0,
                rows=[],
            )

        total_stmt = select(func.count()).select_from(TitanicPassengerOrm).where(
            TitanicPassengerOrm.source_file == selected_source
        )
        total = int((await self._db.scalar(total_stmt)) or 0)
        total_pages = ceil(total / normalized_size) if total else 0
        safe_page = min(normalized_page, total_pages) if total_pages else 1
        offset = (safe_page - 1) * normalized_size

        rows_stmt = (
            select(TitanicPassengerOrm)
            .where(TitanicPassengerOrm.source_file == selected_source)
            .order_by(TitanicPassengerOrm.id.asc())
            .offset(offset)
            .limit(normalized_size)
        )
        rows = (await self._db.execute(rows_stmt)).scalars().all()

        titanic_flow_log(
            "walter-read",
            "5/outbound->pg",
            "selected source_file=%s total=%s page=%s size=%s",
            selected_source,
            total,
            safe_page,
            normalized_size,
        )

        return WalterPassengerPageResponse(
            source_file=selected_source,
            page=safe_page,
            size=normalized_size,
            total=total,
            total_pages=total_pages,
            rows=[
                WalterPassengerItem(
                    id=int(row.id or 0),
                    source_file=row.source_file,
                    passenger_id=row.dataset_passenger_id,
                    survived=row.survived,
                    pclass=row.pclass,
                    name=row.name,
                    gender=row.gender,
                    age=row.age,
                    sib_sp=row.sib_sp,
                    parch=row.parch,
                    ticket=row.ticket,
                    fare=row.fare,
                    created_at=row.created_at.isoformat() if row.created_at else None,
                )
                for row in rows
            ],
        )
