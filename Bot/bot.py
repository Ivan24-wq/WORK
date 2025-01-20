import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging
import os
from dotenv import load_dotenv
from database import (
    create_table,
    add_user_if_not_exists,
    update_user_subscription,
    update_user_city,
    update_user_price,
    get_user_city,
    get_listings_by_city_or_region_and_price,
    get_user_subscription_info,
    get_user_region,
    update_user_region
)
from datetime import datetime

# Загрузка переменных окружения
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = Bot(token=API_TOKEN)

dp = Dispatcher()

# Клавиатуры
finish_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Standart"), KeyboardButton(text="😎 PREMIUM")]],
    resize_keyboard=True
)

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Выберите подписку!"), KeyboardButton(text="Тарифы!")]],
    resize_keyboard=True
)

premium_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="1 месяц - 200р", callback_data="premium_1_month"),
         InlineKeyboardButton(text="3 месяца - 499р", callback_data="premium_3_months")],
        [InlineKeyboardButton(text="1 год - 2200р", callback_data="premium_1_year")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_subscription")]
    ]
)

class UserStates(StatesGroup):
    waiting_for_city_or_region = State()
    waiting_for_price = State()

# Обработчики
@dp.message(Command(commands=["start"]))
async def start_command(message: types.Message):
    add_user_if_not_exists(message.from_user.id)
    await message.answer("Рады вас видеть! \nВыберите свой тарифный план!", reply_markup=start_keyboard)

@dp.message(F.text.in_(["Standart", "😎 PREMIUM"]))
async def subscription_choice(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    selected_subscription = "Standart" if message.text == "Standart" else "Premium"
    
    if selected_subscription == "Standart":
        update_user_subscription(user_id, selected_subscription, 0)  # Standart подписка не имеет срока
        await message.answer("Вы выбрали подписку Standart. Укажите ваш регион.", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="✅ Перейти на PREMIUM")]],
            resize_keyboard=True
        ))
        await state.set_state(UserStates.waiting_for_city_or_region)
    else:
        await message.answer("Вы выбрали подписку Premium. Выберите тариф:", reply_markup=premium_keyboard)

@dp.callback_query(lambda call: call.data.startswith("premium"))
async def handle_premium_tariff(call: types.CallbackQuery, state: FSMContext):
    tariffs = {
        "premium_1_month": (200, 30),
        "premium_3_months": (499, 90),
        "premium_1_year": (2200, 365),
    }

    selected_tariff = tariffs.get(call.data)
    if selected_tariff:
        price, duration = selected_tariff
        update_user_subscription(call.from_user.id, "PREMIUM", duration)

        subscription_type, end_date = get_user_subscription_info(call.from_user.id)
        if end_date and isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        end_date_formatted = end_date.strftime("%d.%m.%Y") if end_date else "Дата окончания неизвестна"

        await call.message.answer(
            f"Тип подписки: {subscription_type}\n"
            f"Дата окончания: {end_date_formatted}\n"
            f"Стоимость: {price} руб.\n"
            f"Спасибо за выбор!"
        )
        await call.message.answer("Укажите город поиска:")
        await state.set_state(UserStates.waiting_for_city_or_region)
    else:
        await call.message.answer("Неизвестный тариф. Пожалуйста, выберите тариф заново.")

@dp.message(lambda message: message.text == "Выберите подписку!")
async def choose_subscription_command(message: types.Message):
    await message.answer("Выберите подписку:", reply_markup=finish_keyboard)

@dp.message(lambda message: message.text == "✅ Перейти на PREMIUM")
async def transition_to_premium(message: types.Message):
    await message.answer("Вы перешли на подписку PREMIUM! Выберите свой тарифный план", reply_markup=premium_keyboard)

@dp.message(UserStates.waiting_for_city_or_region)
async def city_input(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    city_or_region = message.text
    update_user_city(user_id, city_or_region)
    await message.answer("Укажите диапазон цен (например, 1000-5000):")
    await state.set_state(UserStates.waiting_for_price)

@dp.message(UserStates.waiting_for_price)
async def price_input(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        min_price, max_price = map(int, message.text.split('-'))
        city = get_user_city(user_id)
        region = get_user_region(user_id)

        if not city and not region:
            await message.answer("Сначала укажите город или регион.")
            return

        listings = get_listings_by_city_or_region_and_price(city, region, min_price, max_price)

        if listings:
            await message.answer(f"Варианты по цене от {min_price} до {max_price} руб.")
            for description, price, contact, photo in listings:
                await message.answer(
                    f"📋 Описание: {description}\n"
                    f"💵 Цена: {price} руб.\n"
                    f"📞 Контакт: {contact}"
                )
        else:
            await message.answer(f"Нет вариантов по указанному диапазону цен в {city if city else region}.")
    finally:
        await state.clear()

@dp.message(F.text == "Тарифы!")
async def tariffs_command(message: types.Message):
    await message.answer(
        "🗓 Тарифные планы:\n"
        "Standart – поиск по региону.\n"
        "PREMIUM – поиск по городу.\n"
        "📊 Цены:\n"
        "✅ 1 месяц - 200р\n"
        "✅ 3 месяца - 499р\n"
        "✅ 1 год - 2200р"
    )

async def main():
    create_table()
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
