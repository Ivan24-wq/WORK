from aiogram import Dispatcher, types
from aiogram.types import Message

async def standart_subscription(message: Message):
    await message.answer(
        "Вы выбрали подписку Standart!. Ваш функционал ограничен."
    )

async def premium_subscription(message: Message):
    await message.answer(
        "Вы выбрали подписку PREMIUM. Спасибо, что выбрали нашу команду!"
    )

def register_handlers(dp: Dispatcher):
    dp.message.register(standart_subscription, lambda message: message.text == "Standart")
    dp.message.register(premium_subscription, lambda message: message.text == "😎 PREMIUM")
