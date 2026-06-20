from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.schemas import BalanceResponse, DebtResponse
from ..services.debt_service import DebtService

router = APIRouter(tags=["debts"])


@router.get("/api/groups/{group_id}/debts", response_model=list[DebtResponse])
def list_group_debts(group_id: int, db: Session = Depends(get_db)):
    return DebtService(db).list_group_debts(group_id)


@router.get("/api/groups/{group_id}/balance", response_model=BalanceResponse)
def get_group_balance(group_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    return DebtService(db).get_balance(group_id=group_id, user_id=user_id)


@router.post("/api/debts/{debt_id}/settle")
def settle_debt(debt_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    return DebtService(db).settle(debt_id=debt_id, actor_user_id=user_id)


@router.get("/api/debts/history", response_model=list[DebtResponse])
def debt_history(user_id: int = Query(...), db: Session = Depends(get_db)):
    return DebtService(db).history(user_id)

