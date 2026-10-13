from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.models.transaction import Transaction
from src.models.user import User
from src.routers.accounts import get_db
from src.schemas.finance import TransactionOut
from src.services.auth import current_active_user

router = APIRouter()


@router.get("", response_model=list[TransactionOut])
def list_transactions(

    account_id: str | None = None,
    since: datetime | None = None,
    until: datetime | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    user: User = Depends(current_active_user),
    db: Session = Depends(get_db),
):
    q = db.query(Transaction).filter(Transaction.user_id == user.id)

    if account_id:
        q = q.filter(Transaction.account_id == account_id)
    
    if since:
        q = q.filter(Transaction.created_at >= since)

    if until:
        q = q.filter(Transaction.created_at < until)
    
    return q.order_by(Transaction.created_at.desc()).limit(limit).offset(offset).all()