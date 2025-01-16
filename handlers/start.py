from aiogram import Dispatcher, types
from aiogram.filters import Command
from keyboards.reply import start_keyboard

async def start_command(message: types.Message):
    await message.answer(
        "Рады вас видеть! \nВыберите свой тарифный план!",
        reply_markup=start_keyboard
    )

def register_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command(commands=["start"]))
