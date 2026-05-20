from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.auth_flow_log import auth_log
from secom.app.schemas.user_schema import LoginResponse, UserSchema
from secom.app.services.user_service import UserService


class UserController:
    """HTTP 진입점 — 비즈니스 로직은 Service에 위임."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._service = UserService(db)

    async def save_user(self, user_schema: UserSchema) -> None:
        auth_log(
            "signup",
            "3/controller",
            "→ service.save_user username=%s",
            user_schema.username.strip(),
        )
        await self._service.save_user(user_schema)

    async def login(self, username: str, password: str) -> LoginResponse:
        auth_log("login", "3/controller", "→ service.login username=%s", username.strip())
        return await self._service.login(username, password)
