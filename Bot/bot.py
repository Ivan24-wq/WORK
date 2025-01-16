import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import logging
import datetime
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключаем токен
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = Bot(token=API_TOKEN)

# Создание диспетчера
dp = Dispatcher()

# Создание таблицы БД
def create_table():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subscription TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()

# Функция для добавления пользователя в базу данных
def add_user(name, subscription, phone):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (name, subscription, phone) VALUES (?, ?, ?)", (name, subscription, phone))
    connection.commit()
    connection.close()

# Клавиатура для запроса номера телефона
def phone_request_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Отправить номер телефона", request_contact=True)
    keyboard.add(button)
    return keyboard

# Кнопка старт
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Выберите подписку!")]
    ],
    resize_keyboard=True
)

# Создание кнопок для оформления подписки
finish_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Standart"), KeyboardButton(text="😎 PREMIUM")]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    await message.answer(
        "Рады вас видеть! \nВыберите свой тарифный план!",
        reply_markup=start_keyboard
    )

# Обработчик для подписки Standart
@dp.message(F.text == "Standart")
async def standart_subscription(message: types.Message):
    await message.answer(
        "Вы выбрали подписку Standart! Ваш функционал ограничен."
    )

# Обработчик для подписки PREMIUM
@dp.message(F.text == "😎 PREMIUM")
async def premium_subscription(message: types.Message):
    await message.answer(
        "Вы выбрали подписку PREMIUM. Спасибо, что выбрали нашу команду!"
    )

# Проработка кнопки "Выберите подписку"
@dp.message(lambda message: message.text == "Выберите подписку!")
async def command(message: types.Message):
    await message.answer(
        "Есть два варианта подписки. Standart - бесплатно, объявления доступны в пределах вашего региона. Premium - цена 220р., объявления доступны в пределах города!",
        reply_markup=finish_keyboard
    )

# Запуск бота
async def main():
    # Создаем таблицу перед запуском бота
    create_table()

    # Удаляем старые вебхуки и запускаем поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
#