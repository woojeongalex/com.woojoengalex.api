from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.schemas.user_schema import LoginResponse, UserSchema
from secom.app.services.user_service import UserService


class UserController:
    """HTTP 진입점 — 비즈니스 로직은 Service에 위임 (얇은 컨트롤러)."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._service = UserService(db)

    async def save_user(self, user_schema: UserSchema) -> None:
        await self._service.save_user(user_schema)

    async def login(self, username: str, password: str) -> LoginResponse:
        return await self._service.login(username, password)
