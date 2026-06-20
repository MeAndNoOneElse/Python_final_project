from pydantic import BaseModel
from typing import Optional


class ReceiptItem(BaseModel):
    id: int
    receipt_id: int
    name: str
    price: float
    assigned_to_user_id: Optional[int] = None
