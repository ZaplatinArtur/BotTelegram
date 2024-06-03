from aiogram import Bot
from aiogram.types import Message

async def updating(message: Message):
    await message.answer("Пришлите фото класса")


async def message_text(message: Message):
    await message.photo[-1].download('img/am.jpg')

