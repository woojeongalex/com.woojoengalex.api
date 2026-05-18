from secom.app.schemas.user_schema import UserSchema
from secom.app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        pass

    def save_user(self, user_schema: UserSchema):
        print(
            "[SECOM][Service] save_user layer:",
            {
                "username": user_schema.username,
                "nickname": user_schema.nickname,
                "email": user_schema.email,
                "role": user_schema.role,
                "password_length": len(user_schema.password),
            },
            flush=True,
        )
        user_repository = UserRepository()
        return user_repository.save_user(user_schema)