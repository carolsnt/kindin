"""Auth router — Telegram Login Widget validation."""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from kindin_api.config import settings
from kindin_api.deps import get_db
from kindin_api.models.user import User
from kindin_api.schemas.auth import TelegramAuthPayload, TokenResponse
from kindin_api.security import create_access_token, verify_telegram_auth

router = APIRouter()


@router.post("/telegram", response_model=TokenResponse)
def telegram_login(payload: TelegramAuthPayload, db: Session = Depends(get_db)):
    """Validate Telegram Login Widget hash and return a JWT."""
    if settings.ENV != "development":
        if not verify_telegram_auth(payload.model_dump(), settings.TELEGRAM_BOT_TOKEN):
            raise HTTPException(status_code=401, detail="Invalid Telegram auth hash")

    user = db.query(User).filter(User.telegram_id == payload.id).first()
    if user is None:
        user = User(
            id=uuid.uuid4(),
            telegram_id=payload.id,
            username=payload.username,
            first_name=payload.first_name,
            last_name=payload.last_name,
            photo_url=payload.photo_url,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.username = payload.username
        user.first_name = payload.first_name
        user.last_name = payload.last_name
        user.photo_url = payload.photo_url
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, user_id=str(user.id))
