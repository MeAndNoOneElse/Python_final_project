from sqlalchemy.orm import Session

from ..user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_telegram_id(self, telegram_id: int):
        return self.db.query(User).filter(User.telegram_id == telegram_id).first()

    def create_or_update(self, telegram_id: int, name: str, username: str | None):
        user = self.get_by_telegram_id(telegram_id)
        if user:
            user.name = name
            user.username = username
            self.db.flush()
            return user

        user = User(telegram_id=telegram_id, name=name, username=username)
        self.db.add(user)
        self.db.flush()
        return user

    def update(self, user: User, **fields):
        for key, value in fields.items():
            setattr(user, key, value)
        self.db.flush()
        return user

