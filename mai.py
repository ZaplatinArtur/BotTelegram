import logging
import cv2

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ContentType,Message
import asyncio
from core.utils.comands import set_commands
from concurrent.futures import ThreadPoolExecutor
import time
from aiogram.dispatcher.filters import Command,CommandStart
from date_ref import *
import read_plickers
from core.keybor.reply import start_kb
# Укажите ваш токен
API_TOKEN = '7308674590:AAHJnGGqNAJocdqJMUKpvUicAVIyG406nk4'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    #await set_commands(bot)
    await message.answer('Бот для распознования объектов',reply_markup=start_kb)

@dp.message_handler(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    # Получаем файл

    photo = message.photo[-1]  # Берем фото самого высокого качества
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Скачиваем файл
    destination = f"downloads/{file_id}"
    await bot.download_file(file_path, destination)


    await message.reply("Фото сохранено!")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, read_plickers.scan_photo,destination)
    await message.reply(result)

@dp.message_handler(content_types=[types.ContentType.VIDEO])
async def handle_video(message: types.Message):
    file_id = message.video.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    destination = f'videos/{file_id}.mp4'
    await bot.download_file(file_path, destination)
    await message.reply("Видео сохранено!")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, read_plickers.scan_video_stream, destination)
    await message.reply(result)
    print(0)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)