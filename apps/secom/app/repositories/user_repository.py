from secom.app.schemas.user_schema import UserSchema
from secom.app.models.user_model import UserModel

class UserRepository:
    def __init__(self, db=None):
        self.db = db

    def save_user(self, user_schema: UserSchema):
        print(
            "[SECOM][Repository] save_user layer:",
            {
                "username": user_schema.username,
                "nickname": user_schema.nickname,
                "email": user_schema.email,
                "role": user_schema.role,
                "password_length": len(user_schema.password),
            },
            flush=True,
        )
        user_model = UserModel()
        return user_model.save_user(user_schema)

    async def ensure_tables(self):
        print("[SECOM][Repository] ensure_tables called", flush=True)

    async def exists_by_username(self, username: str) -> bool:
        print(
            "[SECOM][Repository] exists_by_username:",
            {"username": username},
            flush=True,
        )
        return False

    async def exists_by_nickname(self, nickname: str) -> bool:
        print(
            "[SECOM][Repository] exists_by_nickname:",
            {"nickname": nickname},
            flush=True,
        )
        return False