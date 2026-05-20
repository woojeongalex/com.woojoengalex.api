import logging

import bcrypt

logger = logging.getLogger(__name__)


def hash_password(plain: str) -> str:
    # bcrypt는 레이어 6 — DEBUG만 (요청마다 INFO 스팸 방지)
    logger.debug("[AUTH-FLOW][signup][6/model] bcrypt hash")
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    logger.debug("[AUTH-FLOW][login][6/model] bcrypt verify")
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
