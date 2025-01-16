from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопка старт
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Выберите подписку!")]
    ],
    resize_keyboard=True
)

# Кнопки для подписки
finish_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Standart"), KeyboardButton(text="😎 PREMIUM")]
    ],
    resize_keyboard=True
)
