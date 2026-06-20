from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..db.repositories.debt_repository import DebtRepository
from ..db.repositories.expense_repository import ExpenseRepository
from ..db.repositories.group_repository import GroupRepository
from ..models.group import GroupMode
from ..models.receipt import ReceiptStatus
from ..schemas.schemas import ExpenseManualCreate
from .inventory_service import InventoryService
from .shopping_list_service import ShoppingListService


class ExpenseService:
    def __init__(self, db: Session):
        self.db = db
        self.expense_repo = ExpenseRepository(db)
        self.group_repo = GroupRepository(db)
        self.debt_repo = DebtRepository(db)
        self.inventory_service = InventoryService(db)
        self.shopping_service = ShoppingListService(db)

    def create_manual(self, payload: ExpenseManualCreate):
        group = self.group_repo.get(payload.group_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

        expense = self.expense_repo.create_expense(
            group_id=payload.group_id,
            uploaded_by_user_id=payload.uploaded_by_user_id,
            title=payload.title,
            total_amount=payload.total_amount,
            category=payload.category,
            purchase_date=payload.purchase_date,
            is_grocery=payload.is_grocery,
            comment=payload.comment,
        )

        if payload.items:
            for item in payload.items:
                self.expense_repo.add_item(
                    receipt_id=expense.id,
                    name=item.name,
                    price=item.price,
                    quantity=item.quantity,
                    unit=item.unit,
                )

        if payload.is_grocery and payload.storage_location_id and payload.items:
            for item in payload.items:
                self.inventory_service.add_inventory(
                    payload=self.inventory_service_payload(payload.storage_location_id, item.name, item.quantity, item.unit)
                )

        if group.mode == GroupMode.FRIENDS and payload.participant_ids:
            self._create_even_split_debts(expense.id, payload)
            self.expense_repo.set_status(expense, ReceiptStatus.DISTRIBUTED)
        else:
            self.expense_repo.set_status(expense, ReceiptStatus.CONFIRMED)

        self.db.commit()
        self.db.refresh(expense)
        return expense

    @staticmethod
    def inventory_service_payload(storage_id: int, name: str, quantity: float, unit: str):
        from ..schemas.schemas import InventoryAddRequest

        return InventoryAddRequest(
            storage_id=storage_id,
            product_name=name,
            quantity=quantity,
            unit=unit,
            min_threshold=0,
        )

    def _create_even_split_debts(self, expense_id: int, payload: ExpenseManualCreate):
        if payload.uploaded_by_user_id not in payload.participant_ids:
            participants = payload.participant_ids + [payload.uploaded_by_user_id]
        else:
            participants = payload.participant_ids

        if len(participants) <= 1:
            return

        share = round(payload.total_amount / len(participants), 2)
        for participant_id in participants:
            if participant_id == payload.uploaded_by_user_id:
                continue
            self.debt_repo.create(
                group_id=payload.group_id,
                receipt_id=expense_id,
                from_user_id=participant_id,
                to_user_id=payload.uploaded_by_user_id,
                amount=share,
            )

    def list_group_expenses(self, group_id: int):
        return self.expense_repo.list_group_expenses(group_id)

    def get_expense(self, expense_id: int):
        expense = self.expense_repo.get(expense_id)
        if not expense:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
        return expense

    def distribute(self, expense_id: int, assignments: dict[int, int | None]):
        expense = self.get_expense(expense_id)
        if not expense:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

        # Calculate debts based on assignments
        total_amount = expense.total_amount
        payer_id = expense.uploaded_by_user_id

        # Determine which members are participating and their shares
        participating_members = [uid for uid in assignments.keys() if assignments.get(uid) is not None or assignments.get(uid) == 0]

        if not participating_members:
            participating_members = list(assignments.keys())

        # Calculate shares
        fixed_amounts = {uid: amt for uid, amt in assignments.items() if amt is not None}
        fixed_total = sum(fixed_amounts.values())
        remaining = total_amount - fixed_total

        # If there's remaining amount, distribute equally among those without fixed amount
        members_without_fixed = [uid for uid in participating_members if uid not in fixed_amounts]
        if members_without_fixed and remaining > 0:
            equal_share = remaining / len(members_without_fixed)
            for uid in members_without_fixed:
                fixed_amounts[uid] = round(equal_share, 2)

        # Create debts for each participant (they owe money to the payer)
        for member_id, amount in fixed_amounts.items():
            if member_id == payer_id:
                continue
            if amount > 0:
                self.debt_repo.create(
                    group_id=expense.group_id,
                    receipt_id=expense_id,
                    from_user_id=member_id,
                    to_user_id=payer_id,
                    amount=amount,
                )

        self.expense_repo.set_status(expense, ReceiptStatus.DISTRIBUTED)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def confirm_distribution(self, expense_id: int):
        expense = self.get_expense(expense_id)
        self.expense_repo.set_status(expense, ReceiptStatus.CONFIRMED)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def dashboard_stats(self, user_id: int):
        open_debts = self.debt_repo.history_for_user(user_id)
        total_open_debts = sum(d.amount for d in open_debts if not d.is_settled)

        from ..db.group_member import GroupMember
        from ..db.pending_confirmation import PendingConfirmation
        from ..db.inventory import Inventory

        groups_count = self.db.query(GroupMember).filter(GroupMember.user_id == user_id).count()
        pending_confirmations = (
            self.db.query(PendingConfirmation)
            .filter(
                PendingConfirmation.user_id == user_id,
                PendingConfirmation.is_approved.is_(False),
                PendingConfirmation.is_rejected.is_(False),
            )
            .count()
        )
        low_stock_products = self.db.query(Inventory).filter(Inventory.quantity <= Inventory.min_threshold).count()

        return {
            "groups_count": groups_count,
            "total_open_debts": round(total_open_debts, 2),
            "low_stock_products": low_stock_products,
            "pending_confirmations": pending_confirmations,
        }


