from typing import Any, Awaitable, Callable, Dict
import asyncio
from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    """
    Supports an unlimited number of throttling_keys,
    each of which can have its own interval.
    Setup:
        @router.message(..., flags={'throttling_key': 'fast'})   # 3 seconds
        @router.message(..., flags={'throttling_key': 'slow'})   # 30 seconds
    """

    # {key: (TTLCache, ttl_seconds)}
    _configs = {
        "fast": {"ttl": 3, "maxsize": 10_000},
        "slow": {"ttl": 30, "maxsize": 10_000},
        "default": {"ttl": 10, "maxsize": 10_000},
    }

    def __init__(self, bot):
        self.bot = bot

        self.caches: Dict[str, TTLCache] = {}
        self.warned: Dict[str, TTLCache] = {}
        for key, cfg in self._configs.items():
            self.caches[key] = TTLCache(maxsize=cfg["maxsize"], ttl=cfg["ttl"])
            self.warned[key] = TTLCache(maxsize=cfg["maxsize"], ttl=cfg["ttl"])

    async def __call__(  # type: ignore
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        key = get_flag(data, "throttling_key")
        if key not in self.caches:
            return await handler(event, data)

        cache, warned = self.caches[key], self.warned[key]
        chat_id = event.chat.id
        ttl = self._configs[key]["ttl"]

        if chat_id in cache:
            if chat_id not in warned:
                warned[chat_id] = True
                await self.bot.send_message(
                    chat_id, f"Too many requests! Please wait {ttl} seconds."
                )
            return

        cache[chat_id] = None
        asyncio.create_task(self._notify_unlock(chat_id, key, ttl))
        return await handler(event, data)

    async def _notify_unlock(self, chat_id: int, key: str, ttl: int):
        await asyncio.sleep(ttl)
        if chat_id not in self.caches[key]:
            try:
                await self.bot.send_message(chat_id, "You can use the bot again.")
            except Exception:
                pass
