from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.chat_type import ChatType

from app.filters.is_admin import IsAdmin
from app.texts import texts


router = Router()
router.message.filter(IsAdmin(True))


@router.message(Command("admin"), F.chat.type == ChatType.PRIVATE)
async def start(message: Message):
    """Admin Command"""
    await message.reply(texts.ADMIN)
