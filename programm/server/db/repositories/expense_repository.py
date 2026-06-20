from datetime import date

from sqlalchemy.orm import Session

from ...models.receipt import ReceiptStatus
from ..receipt import Receipt
from ..receipt_item import ReceiptItem


class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_expense(
        self,
        group_id: int,
        uploaded_by_user_id: int,
        title: str,
        total_amount: float,
        category: str,
        purchase_date: date | None,
        is_grocery: bool,
        comment: str | None,
    ) -> Receipt:
        expense = Receipt(
            group_id=group_id,
            uploaded_by_user_id=uploaded_by_user_id,
            title=title,
            total_amount=total_amount,
            category=category,
            purchase_date=purchase_date,
            is_grocery=is_grocery,
            comment=comment,
            status=ReceiptStatus.PENDING,
        )
        self.db.add(expense)
        self.db.flush()
        return expense

    def add_item(self, receipt_id: int, name: str, price: float, quantity: float, unit: str) -> ReceiptItem:
        item = ReceiptItem(receipt_id=receipt_id, name=name, price=price, quantity=quantity, unit=unit)
        self.db.add(item)
        self.db.flush()
        return item

    def list_group_expenses(self, group_id: int) -> list[Receipt]:
        return self.db.query(Receipt).filter(Receipt.group_id == group_id).order_by(Receipt.id.desc()).all()

    def get(self, expense_id: int):
        return self.db.query(Receipt).filter(Receipt.id == expense_id).first()

    def get_items(self, expense_id: int) -> list[ReceiptItem]:
        return self.db.query(ReceiptItem).filter(ReceiptItem.receipt_id == expense_id).all()

    def set_status(self, expense: Receipt, status: ReceiptStatus) -> Receipt:
        expense.status = status
        self.db.flush()
        return expense

