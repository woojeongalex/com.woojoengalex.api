"""타이타닉 요청 흐름 로그 — 레이어당 1줄 (inbound → input → output → outbound)."""

import logging

logger = logging.getLogger(__name__)


def titanic_flow_log(flow: str, layer: str, message: str, *args: object) -> None:
    logger.info("[TITANIC-FLOW][%s][%s] " + message, flow, layer, *args)
