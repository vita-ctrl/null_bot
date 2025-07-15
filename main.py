import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.commands import COMMANDS
from app.config import load_config
from app import handlers, middlewares
from app.database.engine import create_sessionmaker
# from app.middlewares import ThrottlingMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("aiogram.event").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# dp.message.middleware(ThrottlingMiddleware(10))


async def main() -> None:
    """Main function for the bot"""

    logger.info("Starting bot...")

    config = load_config()

    sessionmaker = (
        await create_sessionmaker(config.db) if config.db.is_enabled else None
    )

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )

    is_set = await bot.set_my_commands(commands=COMMANDS)

    if is_set:
        logger.info("The commands have been successfully set...")
    else:
        logger.warning("The commands are not set...")

    dp = Dispatcher()

    handlers.setup(dp)
    middlewares.setup(dp, sessionmaker, bot)

    await dp.start_polling(bot, config=config)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.critical("Bot stopped")
