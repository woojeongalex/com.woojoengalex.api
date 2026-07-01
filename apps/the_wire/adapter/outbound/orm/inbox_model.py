from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class InboxModel(Base):
    __tablename__ = "wire_inbox"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sender: Mapped[str] = mapped_column(String(255), index=True)
    subject: Mapped[str] = mapped_column(String(500), default="")
    body: Mapped[str] = mapped_column(Text, default="")
    received_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )
    is_read: Mapped[bool] = mapped_column(default=False)
