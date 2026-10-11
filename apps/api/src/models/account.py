from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.models.base import Base

class Account(Base):

    __tablename__ = "accounts"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    display_name = Column(String, nullable=False)
    account_type = Column(String)
    balance_cents = Column(BigInteger, nullable=False, default=0)
    currency = Column(String(3), default="AUD")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())