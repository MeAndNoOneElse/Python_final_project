from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.schemas import ConfirmationResponse
from ..services.confirmation_service import ConfirmationService

router = APIRouter(prefix="/api/confirmations", tags=["confirmations"])


@router.get("/pending", response_model=list[ConfirmationResponse])
def list_pending_confirmations(user_id: int = Query(...), db: Session = Depends(get_db)):
    return ConfirmationService(db).list_pending(user_id)


@router.post("/{confirmation_id}/approve", response_model=ConfirmationResponse)
def approve_confirmation(confirmation_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    return ConfirmationService(db).approve(confirmation_id=confirmation_id, user_id=user_id)


@router.post("/{confirmation_id}/reject", response_model=ConfirmationResponse)
def reject_confirmation(confirmation_id: int, user_id: int = Query(...), db: Session = Depends(get_db)):
    return ConfirmationService(db).reject(confirmation_id=confirmation_id, user_id=user_id)

