"""Share links router."""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from kindin_api.deps import get_current_user, get_db
from kindin_api.models.user import User

router = APIRouter()


class ShareLinkCreate(BaseModel):
    result_id: uuid.UUID


@router.post("/share-links")
def create_share_link(
    body: ShareLinkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a temporary share link for a result (stub)."""
    raise HTTPException(501, detail="Share links not implemented yet")


@router.get("/s/{token}")
def resolve_share_link(token: str):
    """Public endpoint to download via share link (stub)."""
    raise HTTPException(501, detail="Share links not implemented yet")
