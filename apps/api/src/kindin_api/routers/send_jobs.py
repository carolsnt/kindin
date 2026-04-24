"""Send jobs router."""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from kindin_api.deps import get_current_user, get_db
from kindin_api.models.user import User
from kindin_api.schemas.send_job import SendJobCreate, SendJobItemResponse, SendJobResponse

router = APIRouter()


@router.post("", status_code=201)
def create_send_job(
    body: SendJobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a send job (stub)."""
    raise HTTPException(501, detail="Send jobs not implemented yet")


@router.get("/{job_id}", response_model=SendJobResponse)
def get_send_job(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get send job status (stub)."""
    raise HTTPException(501, detail="Send jobs not implemented yet")


@router.get("/{job_id}/items", response_model=list[SendJobItemResponse])
def get_send_job_items(
    job_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get send job items (stub)."""
    raise HTTPException(501, detail="Send jobs not implemented yet")
