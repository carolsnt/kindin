"""FastAPI application factory."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kindin_api.routers import (
    admin_sources,
    auth,
    destinations,
    downloads,
    searches,
    send_jobs,
    share_links,
)

app = FastAPI(
    title="Kindin API",
    description="API para busca de livros via Telegram e envio ao Kindle.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(destinations.router, prefix="/me/destinations", tags=["destinations"])
app.include_router(admin_sources.router, prefix="/admin/sources", tags=["admin"])
app.include_router(searches.router, prefix="/searches", tags=["searches"])
app.include_router(downloads.router, prefix="/downloads", tags=["downloads"])
app.include_router(share_links.router, tags=["share-links"])
app.include_router(send_jobs.router, prefix="/send-jobs", tags=["send-jobs"])
