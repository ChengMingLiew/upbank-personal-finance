from sqlalchemy.orm import Session
from up_bank_sdk import Client
from src.models.up_connection import UpConnection
from src.services.encryption import decrypt_token

class NoActiveConnection(Exception):
    pass

def get_up_client(db: Session, user_id: str) -> Client:

    connection = (
        db.query(UpConnection)
        .filter(UpConnection.user_id == user_id, UpConnection.status == "active")
        .first()
    )
    if connection is None:
        raise NoActiveConnection(f"No active Up connection for user id: {user_id}.")

    return Client(decrypt_token(connection.encrypted_token))