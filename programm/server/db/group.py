from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String
from sqlalchemy.sql import func
from .database import Base
from ..models.group import GroupMode


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, index=True)
    name = Column(String)
    mode = Column(Enum(GroupMode), nullable=False)
    notifications_enabled = Column(Boolean, default=True)
    auto_shopping_list = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
