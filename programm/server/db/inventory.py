from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func
from .database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    storage_location_id = Column(Integer, ForeignKey("storage_locations.id"))
    product_name = Column(String)
    quantity = Column(Float)
    unit = Column(String, default="pcs")
    min_threshold = Column(Float, default=0)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
