import asyncio
from aiogram import Bot, Dispatcher, types
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


@dp.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    await message.answer("Приветствуем! Рады вас видит дорогой клиент! Выберите услугу")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
