import logging

from fastapi import APIRouter, Depends, HTTPException
from the_wire.adapter.inbound.api.mappers.inbox_mapper import (
    request_to_command as inbox_request_to_command,
)
from the_wire.adapter.inbound.api.mappers.inbox_mapper import (
    result_to_response as inbox_result_to_response,
)
from the_wire.adapter.inbound.api.mappers.watch_mapper import (
    inbox_request_to_filter_command,
    result_to_response,
)
from the_wire.adapter.inbound.api.schemas.inbox_schemas import (
    InboxMailResponse,
    ReceiveMailRequest,
)
from the_wire.adapter.inbound.api.schemas.watch_schemas import WatchStatusResponse
from the_wire.app.ports.input.inbox_use_case import InboxUseCase
from the_wire.app.ports.input.watch_use_case import WatchUseCase
from the_wire.dependencies.inbox_provider import get_inbox_use_case
from the_wire.dependencies.watch_provider import get_watch_use_case

logger = logging.getLogger(__name__)

watcher_router = APIRouter(prefix="/api/the-wire", tags=["the-wire-watch"])


@watcher_router.get("/watch", response_model=WatchStatusResponse)
async def read_watch_status(
    use_case: WatchUseCase = Depends(get_watch_use_case),
) -> WatchStatusResponse:
    result = await use_case.read_status()
    if result is None:
        raise HTTPException(
            status_code=404, detail="Gmail watch가 등록되지 않았습니다."
        )
    return result_to_response(result)


@watcher_router.post("/watch/inbox", response_model=InboxMailResponse)
async def receive_mail_with_policy_filter(
    req: ReceiveMailRequest,
    watcher: WatchUseCase = Depends(get_watch_use_case),
    inbox: InboxUseCase = Depends(get_inbox_use_case),
) -> InboxMailResponse:
    """
    자동 파이프라인:
      1. 정책 필터(watson-policy-filter) 추론
      2. BLOCK → 403 차단
      3. PASS  → InboxInteractor.receive() → pgvector 저장
    """
    filter_cmd = inbox_request_to_filter_command(req)
    filter_result = watcher.filter(filter_cmd)

    logger.info(
        "[Watcher] 정책 필터 결과 verdict=%s score=%.3f sender=%s subject=%s",
        filter_result.verdict,
        filter_result.score,
        req.sender,
        req.subject,
    )

    if filter_result.verdict == "BLOCK":
        raise HTTPException(
            status_code=403,
            detail={
                "verdict": "BLOCK",
                "score": filter_result.score,
                "reason": filter_result.reason,
            },
        )

    result = await inbox.receive(inbox_request_to_command(req))
    return inbox_result_to_response(result)
