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

# Функция для добавления пользователя в БД
def update_user_city(telegram_id, city):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET subscription = ? WHERE telegram_id = ?",(city, telegram_id))
    connection.commit()
    connection.close()

# Функция добавления цены аренды
def update_user_price(telegram_id, price):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE ysers SET subscription = ? WHERE telegram_id = ?",(price, telegram_id))
    connection.commit()
    connection.cursor()

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

class UserStates(StatesGroup):
    waiting_for_city = State()
    waiting_for_price = State()
# Обработчик выбора подписки
@dp.message(F.text.in_(["Standart", "😎 PREMIUM"]))
async def subscription_choice(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    current_subscription = get_user_subscription(user_id)
    selected_subscription = "Standart" if message.text == "Standart" else "Premium"
    
    if current_subscription is None:
        # Если подписка ещё не выбрана
        update_user_subscription(user_id, selected_subscription)
        await message.answer(
            f"Вы выбрали подписку {selected_subscription}! Спасибо за ваш выбор."
        )
        await message.answer(
            f"Вы выбрали подписку {selected_subscription}. Теперь выберите ваш город!"
        
        )
        await state.set_state(UserStates.waiting_for_city)
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

        # Смена подписки

@dp.message(F.text == "Да, сменить подписку")
async def confirm_subscription_change(message: types.Message):
    user_id = message.from_user.id
    selected_supscription = "😎 PREMIUM" if get_user_subscription(user_id) == "Standart" else "Standart"
    update_user_subscription(user_id, selected_supscription)
    await message.answer(
        f"Поздравляем вас! Вы успешно перешли на подписку {selected_supscription}"
    )


    # Отмена смены подписки
@dp.message(F.text == "Отмена")
async def cancel_subscription_change(message: types.Message):
    await message.answer(
        f"Смена подписки отменена!", reply_markup=finish_keyboard
    )

    #Команда город
@dp.message(UserStates.waiting_for_city)
async def city_input(message: types.Message):
    user_id = message.from_user.id
    city = message.text
    update_user_city(user_id, city)
    await message.answer(f"Ваш город {city} Теперь укажите цену аренды")


# Команда цена
@dp.message(UserStates.waiting_for_price)
async def price_input(message: types.Message):
    user_id = message.from_user.id
    price = message.text
    update_user_price(user_id, price)
    await message.answer(f"Указанная цена {price}")

#обработка команды тарифы
@dp.message(lambda message: message.text == "Тарифы!")
async def command(message: types.Message):
    await message.answer(
        "🗓 Тарифные план:\n"
        "📊Цена на подписку:\n"
        "✅1 месяц - 200р\n"
        "✅3 месяца – 499р\n"
        "✅1 год – 2200р/n"
    )
    


@dp.message(lambda message: message.text == "Выберите подписку!")
async def command(message: types.Message):
    await message.answer(
        "Есть два варианта подписки. Standart - бесплатно, объявления доступны в пределах вашего региона. Premium - соответственно платно., объявления доступны в пределах города!",
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