"""Admin sources CRUD router."""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from kindin_api.deps import get_current_user, get_db
from kindin_api.models.source import Source
from kindin_api.models.user import User
from kindin_api.schemas.source import SourceCreate, SourceResponse, SourceUpdate

router = APIRouter()


@router.get("", response_model=list[SourceResponse])
def list_sources(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all sources (admin only)."""
    return db.query(Source).all()


@router.post("", response_model=SourceResponse, status_code=201)
def create_source(
    body: SourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new source."""
    source = Source(id=uuid.uuid4(), added_by_user_id=current_user.id, **body.model_dump())
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@router.patch("/{source_id}", response_model=SourceResponse)
def update_source(
    source_id: uuid.UUID,
    body: SourceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a source."""
    source = db.query(Source).filter(Source.id == source_id).first()
    if source is None:
        raise HTTPException(404, "Source not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(source, field, value)
    db.commit()
    db.refresh(source)
    return source
