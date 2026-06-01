"""James upload — `Titanic-Dataset.csv` 컬럼·응답 스키마."""

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

# CSV 헤더 (Titanic-Dataset.csv 1행)
JAMES_CSV_COLUMNS: tuple[str, ...] = (
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "gender",  # Kaggle CSV는 "Sex" — 아래 has_james_csv_column 참고
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
)

GENDER_CSV_HEADERS = ("gender", "Sex")


def has_james_csv_column(column: str, fieldnames: list[str]) -> bool:
    if column == "gender":
        return any(h in fieldnames for h in GENDER_CSV_HEADERS)
    return column in fieldnames


class JamesSchema(BaseModel):
    """CSV 승객 1행 — 헤더명은 데이터셋 파일과 동일."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    passenger_id: str = Field(alias="PassengerId")
    survived: str = Field(alias="Survived")
    pclass: str = Field(alias="Pclass")
    name: str = Field(alias="Name")
    gender: str = Field(validation_alias=AliasChoices("gender", "Sex"))
    age: str = Field(default="", alias="Age")
    sib_sp: str = Field(alias="SibSp")
    parch: str = Field(alias="Parch")
    ticket: str = Field(default="", alias="Ticket")
    fare: str = Field(alias="Fare")
    cabin: str = Field(default="", alias="Cabin")
    embarked: str = Field(default="", alias="Embarked")

    def to_passenger_row_dict(self) -> dict[str, str]:
        """Use Case·DTO 저장용 (Cabin/Embarked 제외)."""
        return {
            "passenger_id": self.passenger_id,
            "survived": self.survived,
            "pclass": self.pclass,
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "sib_sp": self.sib_sp,
            "parch": self.parch,
            "ticket": self.ticket,
            "fare": self.fare,
        }


class JamesUploadResponse(BaseModel):
    """POST /titanic/james/upload 응답."""

    file_name: str
    count: int
