"""Destinations CRUD router."""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from kindin_api.deps import get_current_user, get_db
from kindin_api.models.destination import Destination
from kindin_api.models.user import User
from kindin_api.schemas.destination import DestinationCreate, DestinationResponse, DestinationUpdate

router = APIRouter()


@router.get("", response_model=list[DestinationResponse])
def list_destinations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all destinations for the current user."""
    return db.query(Destination).filter(Destination.user_id == current_user.id).all()


@router.post("", response_model=DestinationResponse, status_code=201)
def create_destination(
    body: DestinationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new destination for the current user."""
    dest = Destination(id=uuid.uuid4(), user_id=current_user.id, **body.model_dump())
    db.add(dest)
    db.commit()
    db.refresh(dest)
    return dest


@router.patch("/{destination_id}", response_model=DestinationResponse)
def update_destination(
    destination_id: uuid.UUID,
    body: DestinationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a destination."""
    dest = db.query(Destination).filter(
        Destination.id == destination_id, Destination.user_id == current_user.id
    ).first()
    if dest is None:
        raise HTTPException(404, "Destination not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(dest, field, value)
    db.commit()
    db.refresh(dest)
    return dest


@router.delete("/{destination_id}", status_code=204)
def delete_destination(
    destination_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a destination."""
    dest = db.query(Destination).filter(
        Destination.id == destination_id, Destination.user_id == current_user.id
    ).first()
    if dest is None:
        raise HTTPException(404, "Destination not found")
    db.delete(dest)
    db.commit()
