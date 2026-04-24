"""Downloads router."""
import uuid

from fastapi import APIRouter, Depends

from kindin_api.deps import get_current_user
from kindin_api.models.user import User

router = APIRouter()


@router.get("/results/{result_id}")
def download_result(
    result_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
):
    """Download a search result file (not implemented)."""
    from fastapi import HTTPException
    raise HTTPException(501, detail="Download not implemented yet")
