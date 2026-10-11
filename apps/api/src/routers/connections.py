from fastapi import APIRouter, HTTPException, Depends 
from pydantic import BaseModel
from up_bank_sdk import Client
from src.services.encryption import encrypt_token
from src.services.auth import current_active_user
from src.models.user import User
from src.database import SessionLocal
from src.models.up_connection import UpConnection

router = APIRouter()

class ConnectRequest(BaseModel):
    token: str

@router.post("")
def connect_up_account(body: ConnectRequest, user: User = Depends(current_active_user)):
    client = Client(body.token)
    try:
        client.util.ping()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Up Token")

    encrypted = encrypt_token(body.token)

    db = SessionLocal()
    try:
        connection = UpConnection(
            id=user.id,
            user_id=user.id,
            encrypted_token=encrypted,
            status="active",
        )

        db.add(connection)
        db.commit()
    finally:
        db.close()

    return {"status": "connected"}