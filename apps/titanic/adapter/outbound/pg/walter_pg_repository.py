from dataclasses import asdict
from math import ceil
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from titanic.adapter.outbound.orm.titanic_passenger_orm import TitanicPassengerOrm
from titanic.app.dtos.walter_page import WalterPassengerItemDto, WalterPassengerPageDto
from titanic.app.ports.output.walter_repository_port import WalterRepositoryPort
from titanic.app.titanic_flow_log import titanic_flow_log


def _item_from_orm(orm_row: TitanicPassengerOrm) -> WalterPassengerItemDto:
    created_at = orm_row.created_at.isoformat() if orm_row.created_at else None
    return WalterPassengerItemDto(
        id=int(orm_row.id or 0),
        source_file=orm_row.source_file,
        passenger_id=orm_row.dataset_passenger_id,
        survived=orm_row.survived,
        pclass=orm_row.pclass,
        name=orm_row.name,
        gender=orm_row.gender,
        age=orm_row.age,
        sib_sp=orm_row.sib_sp,
        parch=orm_row.parch,
        ticket=orm_row.ticket,
        fare=orm_row.fare,
        created_at=created_at,
    )


def _page_to_dict(page: WalterPassengerPageDto) -> dict[str, Any]:
    body = asdict(page)
    body["rows"] = [asdict(row) for row in page.rows]
    return body


class WalterPgRepository(WalterRepositoryPort):
    db: AsyncSession

    @staticmethod
    async def _resolve_source_file(source_file: str | None) -> str | None:
        if source_file:
            return source_file
        stmt = (
            select(TitanicPassengerOrm.source_file)
            .order_by(TitanicPassengerOrm.id.desc())
            .limit(1)
        )
        return await WalterPgRepository.db.scalar(stmt)

    @staticmethod
    async def read_passengers(
        source_file: str | None, page: int, page_size: int
    ) -> dict[str, Any]:
        page = max(1, page)
        page_size = max(1, min(page_size, 100))
        source_file = await WalterPgRepository._resolve_source_file(source_file)

        if not source_file:
            titanic_flow_log(
                "walter-read",
                "outbound",
                "Neon read empty (no rows in DB) page=%s size=%s",
                page,
                page_size,
                source_file="(none)",
            )
            return _page_to_dict(
                WalterPassengerPageDto(
                    source_file=None,
                    page=page,
                    size=page_size,
                    total=0,
                    total_pages=0,
                    rows=(),
                )
            )

        count_stmt = (
            select(func.count())
            .select_from(TitanicPassengerOrm)
            .where(TitanicPassengerOrm.source_file == source_file)
        )
        total = int((await WalterPgRepository.db.scalar(count_stmt)) or 0)
        total_pages = ceil(total / page_size) if total else 0
        page = min(page, total_pages) if total_pages else 1

        list_stmt = (
            select(TitanicPassengerOrm)
            .where(TitanicPassengerOrm.source_file == source_file)
            .order_by(TitanicPassengerOrm.id.asc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        orm_rows = (await WalterPgRepository.db.execute(list_stmt)).scalars().all()

        titanic_flow_log(
            "walter-read",
            "outbound",
            "Neon read total=%s page=%s size=%s",
            total,
            page,
            page_size,
            source_file=source_file,
        )

        return _page_to_dict(
            WalterPassengerPageDto(
                source_file=source_file,
                page=page,
                size=page_size,
                total=total,
                total_pages=total_pages,
                rows=tuple(_item_from_orm(row) for row in orm_rows),
            )
        )
