from typing import Optional

from fastapi import Request
from fastapi_users import BaseUserManager, exceptions

from src.config import settings
from src.models.user import User


class StringIDMixin:

    def parse_id(self, value) -> str:
        try:
            return str(value)
        except ValueError as e:
            raise exceptions.InvalidID() from e

class UserManager(StringIDMixin, BaseUserManager[User, str]):

    reset_password_token_secret = settings.ENCRYPTION_KEY
    verification_token_secret = settings.ENCRYPTION_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has been registered.")