from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..db.repositories.confirmation_repository import ConfirmationRepository
from ..db.repositories.debt_repository import DebtRepository
from ..models.pending_confirmation import ConfirmationType


class DebtService:
    def __init__(self, db: Session):
        self.db = db
        self.debt_repo = DebtRepository(db)
        self.confirmation_repo = ConfirmationRepository(db)

    def list_group_debts(self, group_id: int):
        return self.debt_repo.list_open_by_group(group_id)

    def get_balance(self, group_id: int, user_id: int):
        total_owed, total_due = self.debt_repo.user_balance(group_id=group_id, user_id=user_id)
        return {
            "user_id": user_id,
            "group_id": group_id,
            "total_owed": total_owed,
            "total_due": total_due,
            "net_balance": total_due - total_owed,
        }

    def settle(self, debt_id: int, actor_user_id: int):
        debt = self.debt_repo.get(debt_id)
        if not debt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debt not found")
        if debt.from_user_id != actor_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only debtor can initiate settlement")

        confirmation = self.confirmation_repo.create(
            user_id=debt.to_user_id,
            confirmation_type=ConfirmationType.SETTLEMENT,
            data={"debt_id": debt.id, "from_user_id": debt.from_user_id, "to_user_id": debt.to_user_id},
        )
        self.db.commit()
        return {"status": "pending_confirmation", "confirmation_id": confirmation.id}

    def history(self, user_id: int):
        return self.debt_repo.history_for_user(user_id)

