import logging

from the_wire.app.dtos.introduce_dto import IntroduceQuery, IntroduceResponse
from the_wire.app.ports.input.introduce_use_case import IntroduceUseCase
from the_wire.app.ports.output.introduce_port import IntroducePort

logger = logging.getLogger(__name__)


class IntroduceInteractor(IntroduceUseCase):
    def __init__(self, repository: IntroducePort) -> None:
        self.repository = repository

    async def introduce_myself(self, query: IntroduceQuery) -> IntroduceResponse:
        logger.info(f"[IntroduceInteractor] introduce_myself | locale={query.locale}")
        return await self.repository.introduce_myself(query)
