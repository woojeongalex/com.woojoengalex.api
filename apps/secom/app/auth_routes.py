"""FastAPI auth 라우트 헬퍼 — main.py 중복 try/except·Repository 생성 통합."""

import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.controllers.user_controller import UserController
from secom.app.exceptions import AuthError
from secom.app.repositories.user_repository import UserRepository
from secom.app.schemas.user_schema import (
    LoginRequest,
    LoginResponse,
    SignupRequest,
    SignupResponse,
    UserSchema,
    UsernameCheckResponse,
)

logger = logging.getLogger(__name__)


def _db_http_error(exc: SQLAlchemyError, context: str) -> HTTPException:
    logger.exception("%s DB 오류: %s", context, exc)
    return HTTPException(
        status_code=503,
        detail="DB 연결에 실패했습니다. 서버 로그를 확인하세요.",
    )


async def check_username_available(
    db: AsyncSession, username: str
) -> UsernameCheckResponse:
    normalized = username.strip()
    if not normalized:
        raise HTTPException(status_code=422, detail="아이디를 입력하세요.")
    try:
        taken = await UserRepository(db).exists_by_username(normalized)
        logger.info("[check-id] username=%s available=%s", normalized, not taken)
        return UsernameCheckResponse(available=not taken)
    except SQLAlchemyError as exc:
        raise _db_http_error(exc, "[check-id]") from exc


async def check_nickname_available(
    db: AsyncSession, nickname: str
) -> UsernameCheckResponse:
    normalized = nickname.strip()
    if not normalized:
        raise HTTPException(status_code=422, detail="닉네임을 입력하세요.")
    try:
        taken = await UserRepository(db).exists_by_nickname(normalized)
        logger.info("[check-nickname] nickname=%s available=%s", normalized, not taken)
        return UsernameCheckResponse(available=not taken)
    except SQLAlchemyError as exc:
        raise _db_http_error(exc, "[check-nickname]") from exc


async def signup_user(db: AsyncSession, request: SignupRequest) -> SignupResponse:
    logger.info(
        "[signup] username=%s nickname=%s email=%s",
        request.username.strip(),
        request.nickname.strip(),
        request.email.strip(),
    )
    if request.password_confirm and request.password != request.password_confirm:
        raise HTTPException(status_code=422, detail="비밀번호가 일치하지 않습니다.")

    user_schema = UserSchema(
        username=request.username,
        nickname=request.nickname,
        password=request.password,
        email=request.email,
        role=request.role or "user",
    )
    try:
        await UserController(db).save_user(user_schema)
    except AuthError as exc:
        logger.warning("[signup] 실패 username=%s — %s", user_schema.username, exc)
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        raise _db_http_error(exc, "[signup]") from exc

    logger.info("[signup] 완료 username=%s", user_schema.username)
    return SignupResponse(ok=True, message="회원가입이 완료되었습니다.")


async def login_user(db: AsyncSession, request: LoginRequest) -> LoginResponse:
    username = request.username.strip()
    if not username or not request.password:
        raise HTTPException(status_code=422, detail="아이디와 비밀번호를 입력하세요.")

    logger.info("[login] username=%s", username)
    try:
        result = await UserController(db).login(username, request.password)
        logger.info("[login] 완료 username=%s", username)
        return result
    except AuthError as exc:
        logger.info("[login] 실패 username=%s — %s", username, exc)
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        raise _db_http_error(exc, "[login]") from exc
