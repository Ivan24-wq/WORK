import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import logging
import os
import sqlite3
from dotenv import load_dotenv

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
        telegram_id INTEGER UNIQUE NOT NULL,
        subscription TEXT DEFAULT NULL
    )
    """)
    connection.commit()
    connection.close()

# Функция для добавления пользователя в базу данных (если отсутствует)
def add_user_if_not_exists(telegram_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (telegram_id,))
    connection.commit()
    connection.close()

# Функция для получения текущей подписки пользователя
def get_user_subscription(telegram_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT subscription FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

# Функция для обновления подписки пользователя
def update_user_subscription(telegram_id, subscription):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET subscription = ? WHERE telegram_id = ?", (subscription, telegram_id))
    connection.commit()
    connection.close()

# Клавиатура для выбора подписки
finish_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Standart"), KeyboardButton(text="😎 PREMIUM")]
    ],
    resize_keyboard=True
)

# Кнопка старт
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Выберите подписку!")]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@dp.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    add_user_if_not_exists(message.from_user.id)
    await message.answer(
        "Рады вас видеть! \nВыберите свой тарифный план!",
        reply_markup=start_keyboard
    )

# Обработчик выбора подписки
@dp.message(F.text.in_(["Standart", "😎 PREMIUM"]))
async def subscription_choice(message: types.Message):
    user_id = message.from_user.id
    current_subscription = get_user_subscription(user_id)
    selected_subscription = "Standart" if message.text == "Standart" else "Premium"

    if current_subscription is None:
        # Если подписка ещё не выбрана
        update_user_subscription(user_id, selected_subscription)
        await message.answer(
            f"Вы выбрали подписку {selected_subscription}! Спасибо за ваш выбор."
        )
    elif current_subscription == selected_subscription:
        # Если пользователь повторно выбирает ту же подписку
        await message.answer(
            f"У вас уже активна подписка {current_subscription}."
        )
    else:
        # Если пользователь пытается выбрать другую подписку
        await message.answer(
            f"У вас уже активна подписка {current_subscription}. Хотите сменить её на {selected_subscription}?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Да, сменить подписку"), KeyboardButton(text="Отмена")]
                ],
                resize_keyboard=True
            )
        )
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
