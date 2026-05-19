from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.repositories.user_repository import UserRepository
from secom.app.schemas.user_schema import LoginResponse, UserSchema


class UserService:
    """컨트롤러 ↔ 레포지터리 연결만 담당."""

    def __init__(self, db: AsyncSession | None = None) -> None:
        self._repository = UserRepository(db)

    async def save_user(self, user_schema: UserSchema) -> None:
        await self._repository.save_user(user_schema)

    async def login(self, username: str, password: str) -> LoginResponse:
        return await self._repository.login(username, password)
