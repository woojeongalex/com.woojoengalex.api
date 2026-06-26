from __future__ import annotations

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from sqlmodel import SQLModel

from star_craft.hub.domain.entities.spoke_registry import SpokeStatus


class SpokeRegistryModel(SQLModel, table=True):
    __tablename__ = "star_craft_spoke_registry"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hub_id: Mapped[int] = mapped_column(ForeignKey("star_craft_hub_nodes.id"), nullable=False)
    spoke_name: Mapped[str] = mapped_column(String(100), nullable=False)
    domain_key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    endpoint_prefix: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(
        Enum(SpokeStatus), default=SpokeStatus.PENDING, nullable=False
    )
    registered_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
