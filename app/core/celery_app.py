from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "media_processor",
    broker=settings.broker_url,
    backend=settings.redis_url,
    include=["app.tasks.process_job"],
)
