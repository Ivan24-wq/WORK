from aiogram import Dispatcher, types
from keyboards.reply import finish_keyboard

async def select_plan(message: types.Message):
    await message.answer(
        "Есть два варианты подписки. Standart - бесплатно, объявления доступны в пределах вашего региона. Premium - цена 220р., объявления доступны в пределах города!",
        reply_markup=finish_keyboard
    )

def register_handlers(dp: Dispatcher):
    dp.message.register(select_plan, lambda message: message.text == "Выберите подписку!")
