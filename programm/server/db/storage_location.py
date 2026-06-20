from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from .database import Base


class StorageLocation(Base):
    __tablename__ = "storage_locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"))
    is_default = Column(Boolean, default=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
