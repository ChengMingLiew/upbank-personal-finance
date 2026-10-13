from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from up_bank_sdk import Client

from src.models.account import Account
from src.models.transaction import Transaction


def sync_accounts(db: Session, client: Client, user_id:str) -> None:

    for a in client.accounts.list():
        stmt = insert(Account).values(
            id = a.id,
            user_id = user_id,
            display_name = a.attributes.display_name,
            account_type = a.attributes.account_type,
            balance_cents = a.attributes.balance.value_in_base_units,
            currency = a.attributes.balance.currency_code,
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=[Account.id],
            set_={
                "display_name": stmt.excluded.display_name,
                "balance_cents": stmt.excluded.balance_cents,
            },
        )
        db.execute(stmt)
    db.commit()


def _rel_id(rel: dict | None) -> str | None:
    """Pull the ID out of a JSON:API relationship dict, or None if empty."""
    if not rel:
        return None
    data = rel.get("data")
    return data.get("id") if data else None


def sync_transactions(db: Session, client: Client, user_id: str, since: str | None = None) -> int:

    count = 0

    page = client.transactions.list(page_size=100, since=since)
    while page is not None:
        for t in page.data:
            attrs = t.attributes
            stmt = insert(Transaction).values(
                id = t.id,
                user_id = user_id,
                account_id = _rel_id(t.relationships.account),
                description = attrs.description,
                amount_cents = attrs.amount.value_in_base_units,
                currency = attrs.amount.currency_code,
                status = attrs.status,
                category_id = _rel_id(t.relationships.category),
                created_at = attrs.created_at,
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=[Transaction.id],
                set_={
                    "status": stmt.excluded.status,
                    "amount_cents": stmt.excluded.amount_cents,
                    "description": stmt.excluded.description,
                    "category_id": stmt.excluded.category_id,
                },
            )
            db.execute(stmt)
            count += 1
        db.commit()
        page=page.get_next()
    return count