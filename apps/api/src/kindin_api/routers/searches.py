"""Searches router with SSE streaming."""
import asyncio
import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from kindin_api.deps import get_current_user, get_db
from kindin_api.models.search import Search
from kindin_api.models.search_result import SearchResult
from kindin_api.models.user import User
from kindin_api.schemas.search import PaginatedResults, SearchCreate, SearchResponse, SearchResultResponse

router = APIRouter()


@router.post("", response_model=SearchResponse, status_code=201)
def create_search(
    body: SearchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new search and return its id."""
    search = Search(
        id=uuid.uuid4(),
        user_id=current_user.id,
        query_title=body.title,
        query_author=body.author,
        query_format=body.format,
        status="running",
    )
    db.add(search)
    db.commit()
    db.refresh(search)
    return search


@router.get("/{search_id}/events")
async def search_events(search_id: uuid.UUID, db: Session = Depends(get_db)):
    """SSE endpoint that streams search progress and done events (stub)."""

    search = db.query(Search).filter(Search.id == search_id).first()
    if search is None:
        raise HTTPException(404, "Search not found")

    async def event_generator():
        # Simulated progress event
        await asyncio.sleep(0.1)
        progress = {"scanned_sources": 1, "total_sources": 1, "scanned_messages": 0}
        yield f"event: progress\ndata: {json.dumps(progress)}\n\n"

        await asyncio.sleep(0.4)
        done = {"total_results": 0}
        yield f"event: done\ndata: {json.dumps(done)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/{search_id}/results", response_model=PaginatedResults)
def search_results(
    search_id: uuid.UUID,
    page: int = 1,
    per_page: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return paginated search results."""
    search = db.query(Search).filter(Search.id == search_id, Search.user_id == current_user.id).first()
    if search is None:
        raise HTTPException(404, "Search not found")
    total = db.query(SearchResult).filter(SearchResult.search_id == search_id).count()
    items = (
        db.query(SearchResult)
        .filter(SearchResult.search_id == search_id)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    return PaginatedResults(
        items=[SearchResultResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        per_page=per_page,
    )
