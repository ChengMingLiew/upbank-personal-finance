import uuid
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from src.models.base import Base

class User(SQLAlchemyBaseUserTable[str], Base):

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now())