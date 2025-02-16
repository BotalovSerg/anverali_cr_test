from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command("add"))
async def processing_cmd_add(message: Message):
    """Handler"""
    await message.answer(text="Add task")
