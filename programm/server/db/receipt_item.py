from sqlalchemy import Column, Float, ForeignKey, Integer, String
from .database import Base


class ReceiptItem(Base):
    __tablename__ = "receipt_items"

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"))
    name = Column(String)
    quantity = Column(Float, default=1)
    unit = Column(String, default="pcs")
    price = Column(Float)
    assigned_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
