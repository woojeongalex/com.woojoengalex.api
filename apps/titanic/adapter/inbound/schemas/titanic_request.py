from pydantic import BaseModel, ConfigDict, Field


class TitanicCommandRequest(BaseModel):
    """
    Titanic 단일 레코드 입력 스키마.

    - 모든 타입은 `str`로 고정합니다.
    - 데이터셋 컬럼 `Sex`를 API 도메인 필드명 `gender`로 매핑합니다.
    """

    model_config = ConfigDict(populate_by_name=True)

    passenger_id: str = Field(alias="PassengerId")
    survived: str = Field(alias="Survived")
    pclass: str = Field(alias="Pclass")
    name: str = Field(alias="Name")
    gender: str = Field(alias="Sex")
    age: str = Field(alias="Age")
    sib_sp: str = Field(alias="SibSp")
    parch: str = Field(alias="Parch")
    ticket: str = Field(alias="Ticket")
    fare: str = Field(alias="Fare")

