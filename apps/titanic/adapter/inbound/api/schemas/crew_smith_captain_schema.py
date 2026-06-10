from pydantic import BaseModel, Field


class SmithCaptainSchema(BaseModel):
    id: int = Field(0, description="Captain ID")
    name: str = Field("에드워드 존 스미스", description="Captain's name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "name": "Edward John Smith",
            }
        }
    }
