import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import logging
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Подлючаем токен
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = Bot(token = API_TOKEN)

active_poll = {}

dp = Dispatcher()
#Кнопка старт
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Бесплатные варианты")]
    ],
    resize_keyboard=True
)

@dp.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    await message.answer(
        "Рады вас видеть! \nВыберите свой тарифный план!",
        reply_markup=start_keyboard
    )

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен!")
    await dp.start_polling(bot)
#запуск бота
if __name__ == "__main__":
    asyncio.run(main())