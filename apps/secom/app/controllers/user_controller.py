from secom.app.schemas.user_schema import UserSchema
from secom.app.services.user_service import UserService

class UserController:
    def __init__(self):
        pass

    def save_user(self, user_schema: UserSchema):
        print(
            "[SECOM][Controller] save_user layer:",
            {
                "username": user_schema.username,
                "nickname": user_schema.nickname,
                "email": user_schema.email,
                "role": user_schema.role,
                "password_length": len(user_schema.password),
            },
            flush=True,
        )
        user_service = UserService()
        return user_service.save_user(user_schema)