from sqlalchemy import Boolean, Column, Date, Enum, Float, ForeignKey, Integer, String
from .database import Base
from ..models.receipt import ReceiptStatus


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    uploaded_by_user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    category = Column(String)
    purchase_date = Column(Date)
    is_grocery = Column(Boolean, default=False)
    total_amount = Column(Float)
    comment = Column(String, nullable=True)
    status = Column(Enum(ReceiptStatus), default=ReceiptStatus.PENDING)
