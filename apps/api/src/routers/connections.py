from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from up_bank_sdk import AuthenticationError, Client

from src.database import SessionLocal
from src.models.up_connection import UpConnection
from src.models.user import User
from src.services.auth import current_active_user
from src.services.encryption import encrypt_token

router = APIRouter()

class ConnectRequest(BaseModel):
    token: str

@router.post("")
def connect_up_account(body: ConnectRequest, user: User = Depends(current_active_user)):
    client = Client(body.token)
    try:
        client.util.ping()
    except AuthenticationError:
        raise HTTPException(status_code=400, detail="Invalid Up Token")

    encrypted = encrypt_token(body.token)

    with SessionLocal() as db:

        connection = (
            db.query(UpConnection)
              .filter(UpConnection.user_id == user.id)
              .first()
        )
        
        if connection:
            connection.encrypted_token = encrypted
            connection.status = "active"
            result = "reconnected"
        else:
            db.add(
                UpConnection(
                    user_id=user.id,
                    encrypted_token=encrypted,
                    status="active",
                )
            )
            result = "connected"
        db.commit()
    db = SessionLocal()

    return {"status": result}