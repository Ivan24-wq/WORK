import asyncio
from aiogram import Bot, Dispatcher
import logging
from config import API_TOKEN
from handlers import start, subscription, select_plan

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Регистрация обработчиков
start.register_handlers(dp)
subscription.register_handlers(dp)
select_plan.register_handlers(dp)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
#fg