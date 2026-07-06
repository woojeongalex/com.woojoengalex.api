from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class WatchModel(Base):
    __tablename__ = "wire_watch"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    history_id: Mapped[str] = mapped_column(String(64))
    expiration: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
