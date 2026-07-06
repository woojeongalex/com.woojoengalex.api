import logging

from sqlalchemy.ext.asyncio import AsyncSession
from the_wire.app.dtos.judge_dto import JudgeResult
from the_wire.app.ports.output.judge_repository_port import JudgeRepositoryPort

logger = logging.getLogger(__name__)


class JudgePgRepository(JudgeRepositoryPort):
    """판정 이력 저장소 — wire_judge_log 테이블 (추후 ORM 마이그레이션 예정).

    현재는 in-memory 반환만 제공하며, ORM 모델 추가 후 실제 DB 저장으로 전환한다.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._log: list[JudgeResult] = []

    async def save(self, result: JudgeResult) -> JudgeResult:
        logger.info(
            "[JudgePgRepository] save | verdict=%s sender=%s",
            result.verdict,
            result.sender,
        )
        self._log.append(result)
        return result

    async def find_all(self) -> list[JudgeResult]:
        logger.info("[JudgePgRepository] find_all | count=%d", len(self._log))
        return list(self._log)
