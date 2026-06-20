from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.schemas import ExpenseManualCreate, ExpenseResponse
from ..services.expense_service import ExpenseService

router = APIRouter(tags=["expenses"])


class ExpenseDistributeRequest(BaseModel):
    assignments: dict[int, int | None]


@router.post("/api/expenses/manual", response_model=ExpenseResponse)
def create_manual_expense(payload: ExpenseManualCreate, db: Session = Depends(get_db)):
    return ExpenseService(db).create_manual(payload)


@router.get("/api/groups/{group_id}/expenses", response_model=list[ExpenseResponse])
def list_group_expenses(group_id: int, db: Session = Depends(get_db)):
    return ExpenseService(db).list_group_expenses(group_id)


@router.get("/api/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    return ExpenseService(db).get_expense(expense_id)


@router.post("/api/expenses/{expense_id}/distribute", response_model=ExpenseResponse)
def distribute_expense(expense_id: int, payload: ExpenseDistributeRequest, db: Session = Depends(get_db)):
    return ExpenseService(db).distribute(expense_id, payload.assignments)


@router.post("/api/expenses/{expense_id}/confirm", response_model=ExpenseResponse)
def confirm_expense(expense_id: int, db: Session = Depends(get_db)):
    return ExpenseService(db).confirm_distribution(expense_id)


@router.post("/api/expenses/scan-qr")
def scan_qr_stub():
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="QR parsing is not implemented in MVP")


@router.post("/api/expenses/upload-photo")
def upload_photo_stub():
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="OCR processing is not implemented in MVP")

