from typing import Optional
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class JackTrainerOrm(Base):
    __tablename__ = "titanic_passengers"

    # 왼쪽 타입 힌트와 우측mapped_column의 데이터 타입을 완벽히 일치시킵니다.
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[Optional[int]] = mapped_column(Integer)
    name: Mapped[Optional[str]] = mapped_column(String)
    gender: Mapped[Optional[str]] = mapped_column(String)
    age: Mapped[Optional[float]] = mapped_column(Float) 
    sib_sp: Mapped[Optional[int]] = mapped_column(Integer)
    parch: Mapped[Optional[int]] = mapped_column(Integer)
    survived: Mapped[Optional[int]] = mapped_column(Integer)