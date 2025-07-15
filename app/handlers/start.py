from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums.chat_type import ChatType
from app.texts import texts

router = Router()


@router.message(CommandStart(), F.chat.type == ChatType.PRIVATE)
async def start(message: Message):
    """Start Command"""
    await message.reply(texts.START)
