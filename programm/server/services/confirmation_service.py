from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..db.repositories.confirmation_repository import ConfirmationRepository
from ..db.repositories.debt_repository import DebtRepository
from ..models.pending_confirmation import ConfirmationType


class ConfirmationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ConfirmationRepository(db)
        self.debt_repo = DebtRepository(db)

    def list_pending(self, user_id: int):
        return self.repo.list_pending_for_user(user_id)

    def approve(self, confirmation_id: int, user_id: int):
        item = self.repo.get(confirmation_id)
        if not item or item.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Confirmation not found")

        if item.type == ConfirmationType.SETTLEMENT:
            debt_id = item.data.get("debt_id")
            debt = self.debt_repo.get(debt_id)
            if debt:
                self.debt_repo.settle(debt)

        self.repo.approve(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def reject(self, confirmation_id: int, user_id: int):
        item = self.repo.get(confirmation_id)
        if not item or item.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Confirmation not found")
        self.repo.reject(item)
        self.db.commit()
        self.db.refresh(item)
        return item

