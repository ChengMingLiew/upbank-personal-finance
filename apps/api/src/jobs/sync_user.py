from datetime import timedelta

from sqlalchemy import func
from up_bank_sdk import AuthenticationError, RateLimitError, ServerError

from src.database import SessionLocal
from src.jobs.celery_app import celery_app
from src.models.transaction import Transaction
from src.models.up_connection import UpConnection
from src.services.sync import sync_accounts, sync_transactions
from src.services.up_client import NoActiveConnection, get_up_client


@celery_app.task(
    bind=True,
    autoretry_for=(RateLimitError, ServerError),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=5,
)

def sync_user(self, user_id: str, full: bool = False) -> dict:

    with SessionLocal() as db:
        try:
            client = get_up_client(db, user_id)
            sync_accounts(db, client, user_id)

            since = None
            if not full:
                latest = (
                    db.query(func.max(Transaction.created_at))
                    .filter(Transaction.user_id == user_id)
                    .scalar()
                )
                if latest:
                    since = (latest - timedelta(days=7)).isoformat()

            count = sync_transactions(db, client, user_id, since=since)
            return {"status": "ok", "transactions": count}

        except NoActiveConnection:
            return {"status": "no_active_connection"}

        except AuthenticationError:
            db.rollback()
            conn = (
                db.query(UpConnection)
                .filter(UpConnection.user_id == user_id, UpConnection.status == "active")
                .first()
            )
            if conn:
                conn.status = "needs_reauth"
                db.commit()
            return {"status": "needs_reauth"}