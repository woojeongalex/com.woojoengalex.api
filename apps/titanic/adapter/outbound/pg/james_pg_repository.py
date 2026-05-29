import logging
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import delete

from titanic.adapter.outbound.orm.titanic_passenger_orm import TitanicPassengerOrm
from titanic.app.dtos.passenger_row import PassengerRowDto
from titanic.app.ports.output.james_repository_port import JamesRepositoryPort
from titanic.app.titanic_flow_log import titanic_flow_log

logger = logging.getLogger(__name__)


class JamesPgRepository(JamesRepositoryPort):
    db: AsyncSession

    @staticmethod
    async def save_upload(
        file_name: str, records: list[dict[str, Any]]
    ) -> dict[str, Any]:
        passengers = [PassengerRowDto(**row) for row in records]
        orm_rows = [
            TitanicPassengerOrm.from_passenger_row(file_name, passenger)
            for passenger in passengers
        ]
        titanic_flow_log(
            "james-upload",
            "outbound",
            "Neon replace rows=%s",
            len(orm_rows),
            source_file=file_name,
        )
        try:
            await JamesPgRepository.db.execute(delete(TitanicPassengerOrm))
            JamesPgRepository.db.add_all(orm_rows)
            await JamesPgRepository.db.commit()
        except Exception:
            await JamesPgRepository.db.rollback()
            logger.exception(
                "[TITANIC-FLOW][james-upload][outbound] source_file=%s | commit failed rows=%s",
                file_name,
                len(orm_rows),
            )
            raise

        return {"file_name": file_name, "count": len(orm_rows)}
