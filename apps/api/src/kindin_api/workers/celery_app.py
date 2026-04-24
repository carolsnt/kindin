"""Celery application configuration."""
from celery import Celery

from kindin_api.config import settings

celery_app = Celery(
    "kindin",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["kindin_api.workers.telegram_search", "kindin_api.workers.email_sender"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
