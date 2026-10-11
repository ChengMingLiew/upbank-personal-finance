from celery import Celery
from src.config import settings

celery_app = Celery(
    "upbank-personal-finance",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["src.jobs.sync_user"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)