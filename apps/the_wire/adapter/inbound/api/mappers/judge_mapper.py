from the_wire.adapter.inbound.api.schemas.judge_schema import (
    JudgeRequest,
    JudgeResponse,
)
from the_wire.app.dtos.judge_dto import JudgeCommand, JudgeResult


def request_to_command(req: JudgeRequest) -> JudgeCommand:
    return JudgeCommand(
        sender=req.sender,
        subject=req.subject,
        body=req.body,
        important_client=req.important_client,
    )


def result_to_response(result: JudgeResult) -> JudgeResponse:
    return JudgeResponse(
        verdict=result.verdict,
        sender=result.sender,
        subject=result.subject,
        reason=result.reason,
        judged_at=result.judged_at.isoformat(),
    )
