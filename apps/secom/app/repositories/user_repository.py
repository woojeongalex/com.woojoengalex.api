from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.auth_flow_log import auth_log
from secom.app.entities.user_entity import UserEntity
from secom.app.exceptions import AuthError
from secom.app.models.user_model import hash_password, verify_password
from secom.app.schemas.user_schema import LoginResponse, UserSchema


class UserRepository:
    def __init__(self, db: AsyncSession | None = None) -> None:
        self.db = db

    def _require_db(self) -> AsyncSession:
        if self.db is None:
            raise RuntimeError("DB session is not available.")
        return self.db

    async def _exists(self, column, value: str) -> bool:
        db = self._require_db()
        normalized = value.strip().lower()
        stmt = select(UserEntity.id).where(func.lower(column) == normalized)
        return (await db.execute(stmt)).scalar_one_or_none() is not None

    async def save_user(self, user_schema: UserSchema) -> None:
        db = self._require_db()
        username = user_schema.username.strip()

        if await self._exists(UserEntity.username, username):
            raise AuthError("이미 사용 중인 아이디입니다.")
        if await self._exists(UserEntity.nickname, user_schema.nickname):
            raise AuthError("이미 사용 중인 닉네임입니다.")

        auth_log("signup", "5/repository", "Neon INSERT users username=%s", username)
        entity = UserEntity(
            username=username,
            nickname=user_schema.nickname.strip(),
            email=user_schema.email.strip(),
            password_hash=hash_password(user_schema.password),
            role="user",
        )
        db.add(entity)
        await db.commit()
        await db.refresh(entity)
        auth_log("signup", "5/repository", "Neon commit 완료 username=%s", username)

    async def exists_by_username(self, username: str) -> bool:
        return await self._exists(UserEntity.username, username)

    async def exists_by_nickname(self, nickname: str) -> bool:
        return await self._exists(UserEntity.nickname, nickname)

    async def login(self, username: str, password: str) -> LoginResponse:
        normalized = username.strip()
        auth_log("login", "5/repository", "Neon SELECT users username=%s", normalized)

        stmt = select(UserEntity).where(
            func.lower(UserEntity.username) == normalized.lower()
        )
        row = (await self._require_db().execute(stmt)).scalar_one_or_none()

        if row is None or not verify_password(password, row.password_hash):
            raise AuthError("아이디 또는 비밀번호가 올바르지 않습니다.")

        auth_log("login", "5/repository", "검증 성공 username=%s", row.username)
        return LoginResponse(
            ok=True,
            message="로그인되었습니다.",
            username=row.username,
            nickname=row.nickname,
            role=row.role,
        )
