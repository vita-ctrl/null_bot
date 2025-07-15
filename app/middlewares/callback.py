"""Callback middleware"""

from contextlib import suppress
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, exceptions
from aiogram.types import CallbackQuery


class CallbackMiddleware(BaseMiddleware):
    """
    Middleware for answering untouched callback queries.
    """

    async def __call__(  # type: ignore
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        call: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        """Callback middleware"""
        await handler(call, data)
        with suppress(exceptions.TelegramAPIError):
            await call.answer()
