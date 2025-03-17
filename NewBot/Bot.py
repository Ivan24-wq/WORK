import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from dotenv import load_dotenv  
import os
import logging


load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Клавиатура
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Выберите услугу!")]],
    resize_keyboard=True
)

# Обработчик текстового сообщения "Привет"
@dp.message(lambda message: message.text == "Привет")
async def service(message: types.Message):
    await message.answer("Привет! Выберите услугу:", reply_markup=start_keyboard)

# Обработчик команды "/start"
@dp.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    await message.answer(
        "Приветствуем! Рады вас видеть, дорогой клиент! Выберите услугу:",
        reply_markup=start_keyboard
    )

# Главная функция
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен!")
    await dp.start_polling(bot)

# Запуск
if __name__ == "__main__":
    asyncio.run(main())
