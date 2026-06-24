from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.schemas import UserResponse, UserSettingsUpdate
from ..services.user_service import UserService

router = APIRouter(tags=["users"])


class UserCreate(BaseModel):
    telegram_id: int
    name: str
    username: str | None = None


@router.get("/me", response_model=UserResponse)
def get_me(telegram_id: int = Query(...), db: Session = Depends(get_db)):
    """Get current user by telegram ID"""
    return UserService(db).get_current_user(telegram_id)


@router.post("/", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Create or update user by telegram ID"""
    return UserService(db).upsert_current_user(
        telegram_id=payload.telegram_id,
        name=payload.name,
        username=payload.username
    )


@router.put("/me", response_model=UserResponse)
def update_me(
    payload: UserSettingsUpdate,
    telegram_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """Update user settings"""
    return UserService(db).update_settings(telegram_id=telegram_id, payload=payload)

# Users API
