from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from ...models.pending_confirmation import ConfirmationType
from ..pending_confirmation import PendingConfirmation


class ConfirmationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, confirmation_type: ConfirmationType, data: dict, ttl_hours: int = 24) -> PendingConfirmation:
        item = PendingConfirmation(
            user_id=user_id,
            type=confirmation_type,
            data=data,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=ttl_hours),
        )
        self.db.add(item)
        self.db.flush()
        return item

    def get(self, confirmation_id: int):
        return self.db.query(PendingConfirmation).filter(PendingConfirmation.id == confirmation_id).first()

    def list_pending_for_user(self, user_id: int) -> list[PendingConfirmation]:
        now = datetime.now(timezone.utc)
        return (
            self.db.query(PendingConfirmation)
            .filter(
                PendingConfirmation.user_id == user_id,
                PendingConfirmation.expires_at > now,
                PendingConfirmation.is_approved.is_(False),
                PendingConfirmation.is_rejected.is_(False),
            )
            .order_by(PendingConfirmation.created_at.desc())
            .all()
        )

    def approve(self, item: PendingConfirmation) -> PendingConfirmation:
        item.is_approved = True
        item.processed_at = datetime.now(timezone.utc)
        self.db.flush()
        return item

    def reject(self, item: PendingConfirmation) -> PendingConfirmation:
        item.is_rejected = True
        item.processed_at = datetime.now(timezone.utc)
        self.db.flush()
        return item

