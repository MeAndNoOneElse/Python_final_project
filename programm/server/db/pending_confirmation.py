from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, JSON
from sqlalchemy.sql import func
from .database import Base
from ..models.pending_confirmation import ConfirmationType


class PendingConfirmation(Base):
    __tablename__ = "pending_confirmations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(Enum(ConfirmationType))
    data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime)
    is_approved = Column(Boolean, default=False)
    is_rejected = Column(Boolean, default=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)
