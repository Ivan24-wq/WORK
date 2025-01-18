import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import logging
import os
import sqlite3
from dotenv import load_dotenv
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import (
    create_table,
    add_user_if_not_exists,
    get_user_subscription,
    update_user_subscription,
    update_user_city,
    update_user_price
)

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключаем токен
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = Bot(token=API_TOKEN)

# Создание диспетчера
dp = Dispatcher()



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
        [KeyboardButton(text="Выберите подписку!"), KeyboardButton(text="Тарифы!")]
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

# Интерактивные кнопки с тарифами для премикм
premium_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1 месяц - 200р", callback_data="premium_1_month"),
            InlineKeyboardButton(text="3 месяца - 499р", callback_data="premium_3_months"),
        ],
        [
            InlineKeyboardButton(text="1 год - 2200р", callback_data="premium_1_year"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="back_to_subscription"),
        ],
    ]
)

class UserStates(StatesGroup):
    waiting_for_city_or_region = State()
    waiting_for_price = State()

# Обработчик выбора подписки
# Обработчик выбора подписки
@dp.message(F.text.in_(["Standart", "😎 PREMIUM"]))
async def subscription_choice(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    selected_subscription = "Standart" if message.text == "Standart" else "Premium"

    # Обновляем подписку пользователя
    update_user_subscription(user_id, selected_subscription)

    if selected_subscription == "Standart":
        await message.answer("Вы выбрали подписку Standart. Пожалуйста, укажите ваш регион.", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(UserStates.waiting_for_city_or_region)
    elif selected_subscription == "Premium":
        await message.answer("Вы выбрали подписку Premium. Теперь выберите тариф:", reply_markup=premium_keyboard)


# Обработка тарифа PREMIUM
@dp.callback_query(lambda call: call.data.startswith("premium"))
async def handle_premium_tariff(call: types.CallbackQuery, state: FSMContext):
    if call.data == "premium_1_month":
        await call.message.answer("Вы выбрали тариф 1 месяц - 200р. Пожалуйста, укажите ваш город.")
    elif call.data == "premium_3_months":
        await call.message.answer("Вы выбрали тариф 3 месяца - 499р. Пожалуйста, укажите ваш город.")
    elif call.data == "premium_1_year":
        await call.message.answer("Вы выбрали тариф 1 год - 2200р. Пожалуйста, укажите ваш город.")

    # Устанавливаем состояние для ожидания города
    await state.set_state(UserStates.waiting_for_city_or_region)


# Команда смены подписки
@dp.message(F.text == "Да, сменить подписку")
async def confirm_subscription_change(message: types.Message):
    user_id = message.from_user.id
    current_subscription = get_user_subscription(user_id)
    
    # Меняем подписку на противоположную
    new_subscription = "Premium" if current_subscription == "Standart" else "Standart"
    update_user_subscription(user_id, new_subscription)

    await message.answer(
        f"Подписка успешно изменена на {new_subscription}!",
        reply_markup=finish_keyboard
    )


# Обработка команды "Выберите подписку!"
@dp.message(lambda message: message.text == "Выберите подписку!")
async def choose_subscription_command(message: types.Message):
    await message.answer(
        "Выберите подписку:",
        reply_markup=finish_keyboard
    )

# Ожидание города
@dp.message(UserStates.waiting_for_city_or_region)
async def city_input(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    location = message.text

    # Сохраняем город в базу
    update_user_city(user_id, location)

    await message.answer(f"Ваш город: {location}. Теперь укажите цену аренды!")
    await state.set_state(UserStates.waiting_for_price)
# Ожидание цены
@dp.message(UserStates.waiting_for_price)
async def price_input(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    price = message.text

    # Сохраняем цену в базу
    update_user_price(user_id, price)

    await message.answer(f"Указанная цена: {price}. Подбираем варианты!")
    await state.clear()
@dp.message(F.text == "Тарифы!")
async def tariffs_command(message: types.Message):
    await message.answer(
        "🗓 Тарифные планы: Standart- поиск в пределах удазанного ркгиона. PREMIUM – поиск в пределах указанного города\n"
        "📊 Цена подписки:\n"
        "✅ 1 месяц - 200р\n"
        "✅ 3 месяца - 499р\n"
        "✅ 1 год - 2200р\n"
    )


# Запуск бота
async def main():
    create_table()
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())