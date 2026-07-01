import logging
import os

import httpx

logger = logging.getLogger(__name__)

_TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


class TelegramGateway:
    def __init__(self) -> None:
        self._token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self._chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    @property
    def _enabled(self) -> bool:
        return bool(self._token and self._chat_id)

    async def report(self, message: str) -> None:
        if not self._enabled:
            logger.warning("[TelegramGateway] 토큰 또는 Chat ID 미설정 — 보고 스킵")
            return
        url = _TELEGRAM_API.format(token=self._token)
        payload = {"chat_id": self._chat_id, "text": message, "parse_mode": "HTML"}
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(url, json=payload)
            if not resp.is_success:
                logger.error(
                    "[TelegramGateway] 전송 실패 | status=%s body=%s",
                    resp.status_code,
                    resp.text,
                )
            else:
                logger.info("[TelegramGateway] 보고 완료 | message=%s", message)
