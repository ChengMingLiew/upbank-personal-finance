from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccountOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    id: str
    display_name: str
    account_type: str | None
    balance_cents: int
    currency: str


class TransactionOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    id: str
    account_id: str
    description: str
    amount_cents: int
    currency: str
    status: str
    category_id: str | None
    created_at: datetime