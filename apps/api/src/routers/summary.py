from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, literal_column
from sqlalchemy.orm import Session

from src.models.transaction import Transaction
from src.models.user import User
from src.routers.accounts import get_db
from src.services.auth import current_active_user

router = APIRouter()


class SpendingRow(BaseModel):
    month: str
    category_id: str | None
    spent_cents: int
    transactions: int


@router.get("/spending", response_model=list[SpendingRow])
def spending(

    since: datetime | None = None,
    until: datetime | None = None,
    categorised_only: bool = False,
    user: User = Depends(current_active_user),
    db: Session = Depends(get_db),
):

    month  = func.to_char(Transaction.created_at, literal_column("'YYYY-MM'"))
    spent = -func.sum(Transaction.amount_cents)

    q = db.query(
        month.label("month"),
        Transaction.category_id,
        spent.label("spent_cents"),
        func.count().label("transactions"),
    ).filter(Transaction.user_id == user.id, Transaction.amount_cents < 0)

    if since:
        q = q.filter(Transaction.created_at >= since)

    if until:
        q = q.filter(Transaction.created_at < until)

    if categorised_only:
        q = q.filter(Transaction.category_id.is_not(None))

    rows = q.group_by(month, Transaction.category_id).order_by(month.desc(), spent.desc()).all()

    return [
        SpendingRow(
            month = r.month,
            category_id = r.category_id,
            spent_cents = int(r.spent_cents),
            transactions = r.transactions
        )
        for r in rows
    ]