import sqlite3
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
    cursor.execute("UPDATE users SET subscription = ? WHERE telegram_id = ?",(price, telegram_id))
    connection.commit()
    connection.cursor()