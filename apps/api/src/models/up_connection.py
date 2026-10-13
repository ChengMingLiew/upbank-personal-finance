import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func

from src.models.base import Base


class UpConnection(Base):

    __tablename__ = "up_connection"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    encrypted_token = Column(String, nullable=False)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())