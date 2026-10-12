from src.database import SessionLocal
from src.jobs.celery_app import celery_app
from src.jobs.sync_user import sync_user
from src.models.up_connection import UpConnection


@celery_app.task(ignore_result=True)
def sync_all_users() -> int:

    with SessionLocal() as db:
        user_ids = [
            row[0]
            for row in db.query(UpConnection.user_id)
            .filter(UpConnection.status == "active")
            .distinct()
            .all()
        ]
    for uid in user_ids:
        sync_user.delay(uid)

    return len(user_ids)