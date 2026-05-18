from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    nickname: str
    password: str
    email: str
    role: str


class SignupRequest(UserSchema):
    password_confirm: str | None = None


class SignupResponse(BaseModel):
    ok: bool
    message: str