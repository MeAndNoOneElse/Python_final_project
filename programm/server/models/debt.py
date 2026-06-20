from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Debt(BaseModel):
    id: int
    from_user_id: int
    to_user_id: int
    amount: float
    is_settled: bool
    created_at: Optional[datetime] = None
