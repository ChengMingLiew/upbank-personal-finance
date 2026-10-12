from celery import Celery
from src.config import settings
from celery.schedules import crontab

celery_app = Celery(
    "upbank-personal-finance",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["src.jobs.sync_user", "src.jobs.sync_all",]
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

celery_app.conf.beat_schedule = {
    "sync-all-users": {
        "task": "src.jobs.sync_all.sync_all_users",
        "schedule": crontab(hour=3, minute=0)
    },
}
