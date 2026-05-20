from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.auth_flow_log import auth_log
from secom.app.repositories.user_repository import UserRepository
from secom.app.schemas.user_schema import LoginResponse, UserSchema


class UserService:
    """컨트롤러 ↔ 레포지터리 연결."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._repository = UserRepository(db)

    async def save_user(self, user_schema: UserSchema) -> None:
        auth_log(
            "signup",
            "4/service",
            "→ repository.save_user username=%s",
            user_schema.username.strip(),
        )
        await self._repository.save_user(user_schema)

    async def login(self, username: str, password: str) -> LoginResponse:
        auth_log("login", "4/service", "→ repository.login username=%s", username.strip())
        return await self._repository.login(username, password)
