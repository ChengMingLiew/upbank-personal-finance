from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.models.account import Account
from src.models.user import User
from src.schemas.finance import AccountOut
from src.services.auth import current_active_user

router = APIRouter()


def get_db():
    with SessionLocal() as db:
        yield db

    
@router.get("", response_model=list[AccountOut])
def list_accounts(user: User = Depends(current_active_user), db: Session = Depends(get_db)):
    return db.query(Account).filter(Account.user_id == user.id).all()