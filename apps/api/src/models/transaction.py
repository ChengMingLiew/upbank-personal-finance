from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey, Index
from src.models.base import Base

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    description = Column(String, nullable=False)
    amount_cents = Column(BigInteger, nullable=False)
    currency = Column(String(3), default="AUD")
    status = Column(String, nullable=False)
    category_id = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("ix_transactions_user_created", "user_id", "created_at"),
    )