"""인증 요청 흐름 로그 — 레이어당 1줄만 남겨 터미널 노이즈를 줄입니다."""

import logging

logger = logging.getLogger(__name__)


def auth_log(flow: str, step: str, message: str, *args: object) -> None:
    logger.info("[AUTH-FLOW][%s][%s] " + message, flow, step, *args)
