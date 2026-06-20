
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
from .database import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	telegram_id = Column(Integer, unique=True, index=True, nullable=False)
	name = Column(String, nullable=False)
	username = Column(String, nullable=True)
	language = Column(String, default="en", nullable=False)
	preferred_unit = Column(String, default="pcs", nullable=False)
	notifications_enabled = Column(Boolean, default=True)
	default_storage_id = Column(Integer, ForeignKey("storage_locations.id"), nullable=True)

	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
	updated_at = Column(
		DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
	)

