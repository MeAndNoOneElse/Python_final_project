from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..db.repositories.user_repository import UserRepository
from ..schemas.schemas import UserSettingsUpdate


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def get_current_user(self, telegram_id: int):
        user = self.repo.get_by_telegram_id(telegram_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    def upsert_current_user(self, telegram_id: int, name: str, username: str | None):
        user = self.repo.create_or_update(telegram_id=telegram_id, name=name, username=username)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_settings(self, telegram_id: int, payload: UserSettingsUpdate):
        user = self.get_current_user(telegram_id)
        self.repo.update(user, **payload.model_dump(exclude_unset=True))
        self.db.commit()
        self.db.refresh(user)
        return user
