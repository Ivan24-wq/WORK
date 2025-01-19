import sqlite3

def create_table():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Создаем таблицу listings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            photo BLOB,
            description TEXT,
            price INTEGER NOT NULL DEFAULT 0,
            contact TEXT NOT NULL
        )
    """)

    # Создаем таблицу users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            subscription TEXT NOT NULL,
            city TEXT,
            min_price INTEGER DEFAULT 0,
            max_price INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()
def add_user_if_not_exists(telegram_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (telegram_id,))
    connection.commit()
    connection.close()

def update_user_subscription(telegram_id, subscription):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET subscription = ? WHERE telegram_id = ?", (subscription, telegram_id))
    connection.commit()
    connection.close()

def update_user_city(telegram_id, city):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET city = ? WHERE telegram_id = ?", (city, telegram_id))
    connection.commit()
    connection.close()

def update_user_price(telegram_id, min_price, max_price):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET min_price = ?, max_price = ? WHERE telegram_id = ?", (min_price, max_price, telegram_id))
    connection.commit()
    connection.close()

def get_user_city(telegram_id):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT city FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

def get_listings_by_city_and_price(city, min_price, max_price):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT description, price, contact FROM listings WHERE city = ? AND price BETWEEN ? AND ?", (city, min_price, max_price))
    results = cursor.fetchall()
    connection.close()
    return results
