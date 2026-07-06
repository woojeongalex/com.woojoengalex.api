from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class VisionModel(Base):
    __tablename__ = "vision_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_name: Mapped[str] = mapped_column(String(255))
    label: Mapped[str] = mapped_column(String(255))
    confidence: Mapped[float] = mapped_column(Float)
    analyzed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
