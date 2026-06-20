from pydantic import BaseModel
from enum import Enum


class ReceiptStatus(str, Enum):
    PENDING = "pending"
    DISTRIBUTED = "distributed"
    CONFIRMED = "confirmed"


class Receipt(BaseModel):
    id: int
    group_id: int
    uploaded_by_user_id: int
    total_amount: float
    status: ReceiptStatus
