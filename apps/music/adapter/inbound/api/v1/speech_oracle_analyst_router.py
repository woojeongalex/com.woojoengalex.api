from fastapi import APIRouter, Depends
from music.adapter.inbound.api.deps.music_deps import get_oracle_use_case
from music.adapter.inbound.api.schemas.speech_oracle_analyst_schema import (
    OracleIntroduceResponse,
    OracleIntroduceSchema,
)
from music.app.ports.input.speech_oracle_analyst_use_case import OracleAnalystUseCase

speech_oracle_analyst_router = APIRouter(tags=["music-speech"])


@speech_oracle_analyst_router.get(
    "/api/music/oracle/myself", response_model=OracleIntroduceResponse
)
async def oracle_introduce_myself(
    oracle: OracleAnalystUseCase = Depends(get_oracle_use_case),
) -> OracleIntroduceResponse:
    return await oracle.introduce_myself(
        OracleIntroduceSchema(id=10, name="스피치 오라클 (Oracle)")
    )
