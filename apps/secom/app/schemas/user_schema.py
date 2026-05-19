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

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    ok: bool
    message: str
    username: str | None = None
    nickname: str | None = None
    role: str | None = None


class UsernameCheckResponse(BaseModel):
    available: bool