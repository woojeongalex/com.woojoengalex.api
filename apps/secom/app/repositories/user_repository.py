import logging

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.entities.user_entity import UserEntity
from secom.app.exceptions import AuthError
from secom.app.models.user_model import hash_password, verify_password
from secom.app.schemas.user_schema import LoginResponse, UserSchema

logger = logging.getLogger(__name__)


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
        if await self.exists_by_username(username):
            raise AuthError("이미 사용 중인 아이디입니다.")

        db.add(
            UserEntity(
                username=username,
                nickname=user_schema.nickname.strip(),
                email=user_schema.email.strip(),
                password_hash=hash_password(user_schema.password),
                role=user_schema.role or "user",
            )
        )
        await db.commit()
        logger.info("[UserRepository] save_user — username=%s", username)

    async def exists_by_username(self, username: str) -> bool:
        found = await self._exists(UserEntity.username, username)
        logger.info("[UserRepository] exists_by_username — %s exists=%s", username.strip(), found)
        return found

    async def exists_by_nickname(self, nickname: str) -> bool:
        found = await self._exists(UserEntity.nickname, nickname)
        logger.info("[UserRepository] exists_by_nickname — %s exists=%s", nickname.strip(), found)
        return found

    async def login(self, username: str, password: str) -> LoginResponse:
        normalized = username.strip()
        stmt = select(UserEntity).where(
            func.lower(UserEntity.username) == normalized.lower()
        )
        row = (await self._require_db().execute(stmt)).scalar_one_or_none()

        if row is None or not verify_password(password, row.password_hash):
            logger.info("[UserRepository] login 실패 — username=%s", normalized)
            raise AuthError("아이디 또는 비밀번호가 올바르지 않습니다.")

        logger.info("[UserRepository] login 성공 — username=%s", row.username)
        return LoginResponse(
            ok=True,
            message="로그인되었습니다.",
            username=row.username,
            nickname=row.nickname,
            role=row.role,
        )
