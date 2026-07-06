import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from vision.adapter.outbound.mappers.vision_outbound_mapper import (
    model_to_result,
    result_to_model,
)
from vision.adapter.outbound.orm.vision_model import VisionModel
from vision.app.dtos.vision_dto import VisionResult
from vision.app.ports.output.vision_repository_port import VisionRepositoryPort

logger = logging.getLogger(__name__)


class VisionPgRepository(VisionRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, file_name: str, label: str, confidence: float) -> VisionResult:
        logger.info(
            "[VisionPgRepository] save | file_name=%s label=%s", file_name, label
        )
        row = result_to_model(file_name, label, confidence)
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return model_to_result(row)

    async def find_all(self) -> list[VisionResult]:
        result = await self.session.execute(
            select(VisionModel).order_by(VisionModel.analyzed_at.desc())
        )
        return [model_to_result(m) for m in result.scalars().all()]
