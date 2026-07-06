import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from the_wire.adapter.outbound.orm.watch_model import WatchModel
from the_wire.app.dtos.watch_dto import WatchStatusResult
from the_wire.app.ports.output.watch_repository_port import WatchRepositoryPort

logger = logging.getLogger(__name__)


def _to_result(m: WatchModel) -> WatchStatusResult:
    return WatchStatusResult(
        history_id=m.history_id,
        expiration=m.expiration,
        updated_at=m.updated_at,
    )


class WatchPgRepository(WatchRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_latest(self) -> WatchStatusResult | None:
        logger.info("[WatchPgRepository] find_latest")
        result = await self.session.execute(
            select(WatchModel).order_by(WatchModel.updated_at.desc()).limit(1)
        )
        model = result.scalars().first()
        return _to_result(model) if model else None
