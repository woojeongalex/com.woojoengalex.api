from pydantic import BaseModel, Field


class IntroduceRequestSchema(BaseModel):
    locale: str = Field("ko", description="응답 언어 (ko / en)")

    model_config = {"json_schema_extra": {"example": {"locale": "ko"}}}


class IntroduceResponseSchema(BaseModel):
    agent_name: str
    role: str
    capabilities: list[str]
    version: str
