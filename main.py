import logging
from typing import List

from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types

class States(StatesGroup):
    get_image = State()


API_TOKEN = 'token'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())

main_menu = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)\
        .add("Отправить фото")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer('Добро пожаловать!', reply_markup=main_menu)

@dp.message_handler(content_types=["text"])
async def main_menu_handler(message: types.Message):
    match message.text:
        case "Отправить фото":
            await message.answer('🖼Пришлите изображение')
            await States.crop_image.set()
        case '...': pass
            

@dp.message_handler(is_media_group=True, content_types=[types.ContentType.PHOTO,types.ContentType.DOCUMENT, 'text'], state=States.get_image)
async def state_crop_image(message: types.Message, state: FSMContext, album: List[types.Message]) -> None: 
    match message.content_type:
        case 'photo': 
            for obj in album:
                if obj.photo:
                    file_id = obj.photo[-1]
                else:
                    file_id = obj[obj.content_type]
                await file_id.download(destination_file=f'{message.from_user.id}.jpg')
        case 'document':
            for obj in album:
                if obj.document:
                    file_id = obj.photo[-1]
                else:
                    file_id = obj[obj.content_type]
                await file_id.download(destination_file=f'{message.from_user.id}.jpg')    
        case _:
            await message.answer('⚠️Для обрезки лица небходимо прислать изображение!')
            return await States.crop_image.set()

    await state.finish()

if __name__ == '__main__':
    dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True)