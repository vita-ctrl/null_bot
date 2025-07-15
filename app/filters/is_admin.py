"""Is admin filter"""

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
from app.config import Config


class IsAdmin(Filter):
    """Check if user is an admin"""

    def __init__(self, is_admin: bool = True) -> None:
        """Initialize the IsAdmin filter"""
        self.is_admin = is_admin

    async def __call__(self, update: Message | CallbackQuery, config: Config) -> bool:
        """Check if user is an admin"""
        return bool(update.from_user) and (update.from_user.id in config.bot.admins)
