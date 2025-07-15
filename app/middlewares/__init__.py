from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.middlewares.session import SessionMiddleware
from .callback import CallbackMiddleware
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher, sessionmaker: async_sessionmaker | None, bot: Bot) -> None:
    """Setups all middlewares"""
    dp.callback_query.outer_middleware(CallbackMiddleware())
    if sessionmaker:
        dp.update.outer_middleware(SessionMiddleware(sessionmaker))
    dp.message.middleware(ThrottlingMiddleware(bot))
