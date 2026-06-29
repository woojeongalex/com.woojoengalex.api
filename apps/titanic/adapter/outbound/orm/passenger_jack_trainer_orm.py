from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.theone_base import Base


class JackTrainerOrm(Base):
    __tablename__ = "titanic_passengers"
    __table_args__ = {"extend_existing": True}

    # 왼쪽 타입 힌트와 우측mapped_column의 데이터 타입을 완벽히 일치시킵니다.
    passenger_id: Mapped[str | None] = mapped_column(
        String, primary_key=True, nullable=True
    )
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)
    age: Mapped[float | None] = mapped_column(String, nullable=True)
    sib_sp: Mapped[int | None] = mapped_column(String, nullable=True)
    parch: Mapped[int | None] = mapped_column(String, nullable=True)
    survived: Mapped[int | None] = mapped_column(String, nullable=True)
