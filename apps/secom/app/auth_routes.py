"""인증 비즈니스 로직 — main.py 엔드포인트에서 호출."""

import logging

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.auth_flow_log import auth_log
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


async def _check_available(
    db: AsyncSession,
    *,
    value: str,
    empty_detail: str,
    check_fn,
    label: str,
) -> UsernameCheckResponse:
    normalized = value.strip()
    if not normalized:
        raise HTTPException(status_code=422, detail=empty_detail)
    try:
        taken = await check_fn(UserRepository(db), normalized)
        auth_log(label, "2/auth_routes", "available=%s", not taken)
        return UsernameCheckResponse(available=not taken)
    except SQLAlchemyError as exc:
        raise _db_http_error(exc, f"[{label}]") from exc


async def check_username_available(
    db: AsyncSession, username: str
) -> UsernameCheckResponse:
    return await _check_available(
        db,
        value=username,
        empty_detail="아이디를 입력하세요.",
        check_fn=lambda repo, v: repo.exists_by_username(v),
        label="check-id",
    )


async def check_nickname_available(
    db: AsyncSession, nickname: str
) -> UsernameCheckResponse:
    return await _check_available(
        db,
        value=nickname,
        empty_detail="닉네임을 입력하세요.",
        check_fn=lambda repo, v: repo.exists_by_nickname(v),
        label="check-nickname",
    )


async def signup_user(db: AsyncSession, request: SignupRequest) -> SignupResponse:
    if request.password_confirm and request.password != request.password_confirm:
        raise HTTPException(status_code=422, detail="비밀번호가 일치하지 않습니다.")

    user_schema = UserSchema(
        username=request.username,
        nickname=request.nickname,
        password=request.password,
        email=request.email,
        role="user",  # 클라이언트 role 값 무시 — 항상 일반 사용자
    )
    auth_log(
        "signup",
        "2/auth_routes",
        "→ controller.save_user username=%s",
        user_schema.username.strip(),
    )
    try:
        await UserController(db).save_user(user_schema)
    except AuthError as exc:
        logger.warning("[signup] 실패 username=%s — %s", user_schema.username, exc)
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        raise _db_http_error(exc, "[signup]") from exc

    return SignupResponse(ok=True, message="회원가입이 완료되었습니다.")


async def login_user(db: AsyncSession, request: LoginRequest) -> LoginResponse:
    username = request.username.strip()
    if not username or not request.password:
        raise HTTPException(status_code=422, detail="아이디와 비밀번호를 입력하세요.")

    auth_log("login", "2/auth_routes", "→ controller.login username=%s", username)
    try:
        return await UserController(db).login(username, request.password)
    except AuthError as exc:
        logger.warning("[login] 실패 username=%s — %s", username, exc)
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        raise _db_http_error(exc, "[login]") from exc
