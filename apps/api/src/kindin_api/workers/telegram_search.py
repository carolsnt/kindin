"""Telegram search Celery task (stub)."""
from kindin_api.workers.celery_app import celery_app


@celery_app.task(name="kindin.telegram_search")
def run_telegram_search(search_id: str) -> dict:
    """Run a Telegram search and persist results (stub).
    
    TODO: implementar busca real com Telethon.
    """
    return {"search_id": search_id, "status": "stub"}
