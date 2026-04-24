"""E-mail sender Celery task (stub)."""
from kindin_api.workers.celery_app import celery_app


@celery_app.task(name="kindin.email_sender")
def send_email_job(job_id: str) -> dict:
    """Send files via SMTP for a send_job (stub).
    
    TODO: implementar envio real via SMTP com arquivos do Telegram.
    """
    return {"job_id": job_id, "status": "stub"}
