from datetime import datetime, timezone

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from ..debt import Debt


class DebtRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, group_id: int, receipt_id: int | None, from_user_id: int, to_user_id: int, amount: float) -> Debt:
        debt = Debt(
            group_id=group_id,
            receipt_id=receipt_id,
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            amount=amount,
            is_settled=False,
        )
        self.db.add(debt)
        self.db.flush()
        return debt

    def list_open_by_group(self, group_id: int) -> list[Debt]:
        return self.db.query(Debt).filter(Debt.group_id == group_id, Debt.is_settled.is_(False)).all()

    def get(self, debt_id: int):
        return self.db.query(Debt).filter(Debt.id == debt_id).first()

    def settle(self, debt: Debt) -> Debt:
        debt.is_settled = True
        debt.settled_at = datetime.now(timezone.utc)
        self.db.flush()
        return debt

    def history_for_user(self, user_id: int) -> list[Debt]:
        return (
            self.db.query(Debt)
            .filter(and_(Debt.is_settled.is_(True), (Debt.from_user_id == user_id) | (Debt.to_user_id == user_id)))
            .order_by(Debt.settled_at.desc())
            .all()
        )

    def user_balance(self, group_id: int, user_id: int) -> tuple[float, float]:
        total_owed = (
            self.db.query(func.coalesce(func.sum(Debt.amount), 0.0))
            .filter(Debt.group_id == group_id, Debt.from_user_id == user_id, Debt.is_settled.is_(False))
            .scalar()
        )
        total_due = (
            self.db.query(func.coalesce(func.sum(Debt.amount), 0.0))
            .filter(Debt.group_id == group_id, Debt.to_user_id == user_id, Debt.is_settled.is_(False))
            .scalar()
        )
        return float(total_owed or 0.0), float(total_due or 0.0)

