from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.schemas import DashboardStatsResponse
from ..services.expense_service import ExpenseService

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/dashboard", response_model=DashboardStatsResponse)
def dashboard(user_id: int = Query(...), db: Session = Depends(get_db)):
    return ExpenseService(db).dashboard_stats(user_id)

