import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import delete

from titanic.adapter.inbound.api.schemas.titanic_request import TitanicCommandRequest
from titanic.adapter.outbound.orm.titanic_passenger_orm import TitanicPassengerOrm
from titanic.app.titanic_flow_log import titanic_flow_log

logger = logging.getLogger(__name__)


class JamesPgRepository:
    """PG 어댑터 — CSV row를 Neon `titanic_passengers`에 저장."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def move_uploaded_rows(
        self,
        file_name: str,
        rows: list[TitanicCommandRequest],
    ) -> dict[str, object]:
        entities = [
            TitanicPassengerOrm.from_command(file_name, row) for row in rows
        ]
        titanic_flow_log(
            "james-upload",
            "5/outbound->pg",
            "replace-mode start file=%s rows=%s",
            file_name,
            len(entities),
        )
        try:
            # 업로드 시점에 기존 누적 데이터를 비우고 현재 파일만 유지.
            await self._db.execute(delete(TitanicPassengerOrm))
            self._db.add_all(entities)
            await self._db.commit()
        except Exception as exc:
            await self._db.rollback()
            logger.exception(
                "[TITANIC-FLOW][james-upload][5/outbound->pg] DB commit 실패 file=%s rows=%s error=%s",
                file_name,
                len(entities),
                exc,
            )
            raise

        titanic_flow_log(
            "james-upload",
            "5/outbound->pg",
            "replace-mode commit file=%s saved=%s",
            file_name,
            len(entities),
        )
        return {
            "file_name": file_name,
            "count": len(entities),
            "rows": [],
        }
