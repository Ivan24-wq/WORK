import sqlite3
from datetime import datetime, timedelta

def create_table():
    """Создает таблицы listings и users, если они не существуют."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Создаем таблицу listings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
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
            subscription TEXT DEFAULT 'Standart',
            subscription_expiry DATE,
            region TEXT,
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


def update_user_subscription(user_id, subscription_type, duration_in_days):
    """Обновляет подписку пользователя."""
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        # Вычисляем дату окончания подписки
        end_date = (datetime.now() + timedelta(days=duration_in_days)).strftime("%Y-%m-%d")

        # Обновляем подписку
        cursor.execute("""
            UPDATE users
            SET subscription = ?, subscription_expiry = ?
            WHERE telegram_id = ?
        """, (subscription_type, end_date, user_id))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Ошибка обновления подписки: {e}")
    finally:
        connection.close()





def update_user_city(telegram_id, city):
    """Обновляет город пользователя."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET city = ? WHERE telegram_id = ?", (city, telegram_id))
    connection.commit()
    connection.close()


def update_user_region(telegram_id, region):
    """Обновляет регион пользователя."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET region = ? WHERE telegram_id = ?", (region, telegram_id))
    connection.commit()
    connection.close()


def update_user_price(telegram_id, min_price, max_price):
    """Обновляет минимальную и максимальную цену пользователя."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE users 
        SET min_price = ?, max_price = ? 
        WHERE telegram_id = ?
    """, (min_price, max_price, telegram_id))
    connection.commit()
    connection.close()


def get_user_city_and_region(telegram_id):
    """Возвращает город и регион пользователя по telegram_id."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT city, region 
        FROM users 
        WHERE telegram_id = ?
    """, (telegram_id,))
    result = cursor.fetchone()
    connection.close()
    return result if result else (None, None)

import sqlite3

def get_listings_by_city_or_region_and_price(city, region, min_price, max_price):
    """
    Возвращает список объявлений, соответствующих указанным параметрам (город/регион, диапазон цен).
    """
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        # SQL-запрос для фильтрации объявлений
        if city:
            query = """
                SELECT description, price, contact, photo
                FROM listings
                WHERE city = ? AND price BETWEEN ? AND ?
            """
            cursor.execute(query, (city, min_price, max_price))
        elif region:
            query = """
                SELECT description, price, contact, photo
                FROM listings
                WHERE region = ? AND price BETWEEN ? AND ?
            """
            cursor.execute(query, (region, min_price, max_price))
        else:
            return []

        listings = cursor.fetchall()
        return listings
    except sqlite3.Error as e:
        print(f"Ошибка при получении данных из базы: {e}")
        return []
    finally:
        connection.close()



def get_listings_by_city_and_price(city, min_price, max_price):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("""
        SELECT description, price, contact, photo
        FROM listings
        WHERE city = ? AND price BETWEEN ? AND ?
    """, (city, min_price, max_price))
    result = cursor.fetchall()
    connection.close()
    return result



def add_listing(region, city, description, contact, price, photo=None):
    """Добавляет новое объявление в таблицу listings."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO listings (region, city, description, contact, price, photo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (region, city, description, contact, price, photo))
    connection.commit()
    connection.close()


def load_sample_data():
    """Загружает пример данных в таблицу listings."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Проверяем, есть ли уже данные
    cursor.execute("SELECT COUNT(*) FROM listings")
    count = cursor.fetchone()[0]

    # Если данных нет, добавляем примеры
    if count == 0:
        add_listing(
            region="Московская область",
            city="Москва",
            description="Сдается уютная квартира в центре города",
            contact="+7 900 123-45-67",
            price=50000
        )
        add_listing(
            region="Санкт-Петербург",
            city="Санкт-Петербург",
            description="Квартира в историческом центре",
            contact="+7 900 987-65-43",
            price=45000
        )

    connection.close()


def get_user_city(telegram_id):
    """Возвращает город пользователя по telegram_id."""
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT city FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

def get_user_region(telegram_id):
    """Получает регион пользователя по его telegram_id из таблицы user."""
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT region FROM user WHERE telegram_id = ?", (telegram_id,))
        result = cursor.fetchone()  # Получаем один результат

        # Убедимся, что result - это кортеж (или список)
        if result:
            return result[0]  # Возвращаем первый элемент кортежа
        else:
            return None  # Если данных нет
    except sqlite3.Error as e:
        print(f"Ошибка при получении региона пользователя: {e}")
        return None
    finally:
        connection.close()


from datetime import datetime

def get_user_subscription_info(user_id):
    """Получает информацию о подписке пользователя."""
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT subscription, subscription_expiry
            FROM users
            WHERE telegram_id = ?
        """, (user_id,))
        result = cursor.fetchone()

        if result:
            subscription = result[0]
            expiry_date = result[1]
            
            # Преобразуем строку в объект datetime
            if expiry_date:
                expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")
            
            return subscription, expiry_date

        return "Нет подписки", None
    except sqlite3.Error as e:
        print(f"Ошибка получения подписки: {e}")
        return "Ошибка", None
    finally:
        connection.close()

# Функция для поиска объявлений по региону и диапазону цен
def fetch_listings_by_region_and_price(region, min_price, max_price):
    """
    Выводит объявления, соответствующие региону и диапазону цен.
    """
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        # SQL-запрос с фильтрацией по региону и диапазону цен
        cursor.execute("""
            SELECT * FROM listings
            WHERE region = ? AND price BETWEEN ? AND ?
        """, (region, min_price, max_price))
        
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(f"ID: {row[0]}, Город: {row[1]}, Регион: {row[2]}, Описание: {row[3]}, Цена: {row[4]} руб., Контакт: {row[5]}, Фото: {row[6]}")
        else:
            print(f"Нет вариантов по указанному диапазону цен в регионе {region}.")
    except sqlite3.Error as e:
        print(f"Ошибка при получении данных: {e}")
    finally:
        connection.close()
