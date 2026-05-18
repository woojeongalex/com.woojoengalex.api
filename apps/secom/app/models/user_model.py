class UserModel:
    def __init__(self):
        pass

    def save_user(self, user_schema):
        print(
            "[SECOM][Model] save_user reached:",
            {
                "username": user_schema.username,
                "nickname": user_schema.nickname,
                "email": user_schema.email,
                "role": user_schema.role,
                "password_length": len(user_schema.password),
            },
            flush=True,
        )
        return user_schema
