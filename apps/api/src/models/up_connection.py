import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint, func

from src.models.base import Base


class UpConnection(Base):

    __tablename__ = "up_connection"
    __table_args__ =(UniqueConstraint("user_id", name="uq_up_connection_user_id"),)

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    encrypted_token = Column(String, nullable=False)
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())