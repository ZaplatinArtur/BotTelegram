from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🖼Отправить фото")
        ],
        {
            KeyboardButton(text="Отправить видео")
        }
    ]


)