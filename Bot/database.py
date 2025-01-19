import sqlite3


def create_table():
    """Создает таблицы listings и users, если они не существуют."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Создаем таблицу listings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            photo BLOB,
            description TEXT NOT NULL,
            price INTEGER NOT NULL DEFAULT 0,
            contact TEXT NOT NULL
        )
    """)

    # Создаем таблицу users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            subscription TEXT DEFAULT 'none',
            city TEXT,
            min_price INTEGER DEFAULT 0,
            max_price INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def add_user_if_not_exists(telegram_id):
    """Добавляет пользователя в таблицу users, если его еще нет."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (telegram_id,))
    connection.commit()
    connection.close()


def update_user_subscription(telegram_id, subscription):
    """Обновляет подписку пользователя."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET subscription = ? WHERE telegram_id = ?", (subscription, telegram_id))
    connection.commit()
    connection.close()


def update_user_city(telegram_id, city):
    """Обновляет город пользователя."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET city = ? WHERE telegram_id = ?", (city, telegram_id))
    connection.commit()
    connection.close()


def update_user_price(telegram_id, min_price, max_price):
    """Обновляет минимальную и максимальную цену пользователя."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET min_price = ?, max_price = ? WHERE telegram_id = ?", (min_price, max_price, telegram_id))
    connection.commit()
    connection.close()


def get_user_city(telegram_id):
    """Возвращает город пользователя по telegram_id."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT city FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None


def get_listings_by_city_and_price(city, min_price, max_price):
    """Возвращает объявления из таблицы listings, фильтруя по городу и диапазону цен."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT description, price, contact 
        FROM listings 
        WHERE city = ? AND price BETWEEN ? AND ?
    """, (city, min_price, max_price))
    results = cursor.fetchall()
    connection.close()
    return results


def add_listing(city, description, contact, price, photo=None):
    """Добавляет новое объявление в таблицу listings."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO listings (city, description, contact, price, photo)
        VALUES (?, ?, ?, ?, ?)
    """, (city, description, contact, price, photo))
    connection.commit()
    connection.close()


def load_sample_data():
    """Загружает пример данных в таблицу listings."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Проверяем, есть ли уже данные
    cursor.execute("SELECT COUNT(*) FROM listings WHERE city = ?", ("Москва",))
    count = cursor.fetchone()[0]

    # Если данных нет, добавляем пример
    if count == 0:
        add_listing(
            city="Москва",
            description="Сдается уютная квартира с видом на парк",
            contact="+7 900 123-45-67",
            price=45000
        )

    connection.close()
