import sqlite3
from aiogram.types import InputFile

# Создание таблицы `listings` для объявлений
def create_listings_table():
    """Создаёт таблицу listings с колонками для региона и фото, если её нет."""
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                region TEXT,
                description TEXT NOT NULL,
                price INTEGER NOT NULL,
                contact TEXT NOT NULL,
                photo TEXT
            )
        """)
        connection.commit()
        print("Таблица 'listings' успешно создана или уже существует.")
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        connection.close()

# Создание таблицы `user` для сохранения данных о пользователях
def create_user_table():
    """Создаёт таблицу user для сохранения данных о пользователях, если её нет."""
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                telegram_id INTEGER PRIMARY KEY,
                region TEXT
            )
        """)
        connection.commit()
        print("Таблица 'user' успешно создана или уже существует.")
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")
    finally:
        connection.close()

# Добавление объявления в таблицу listings
def add_listing_to_database(city, region, description, price, contact, photo):
    """Добавляет запись в таблицу listings с учётом региона и фото."""
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO listings (city, region, description, price, contact, photo)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (city, region, description, price, contact, photo))

        connection.commit()
        print(f"Объявление добавлено: {city}, {region}, {description}, {price} руб., {contact}, {photo}")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении объявления: {e}")
    finally:
        connection.close()

# Получение всех объявлений из таблицы listings
def fetch_listings():
    """Выводит все записи из таблицы listings."""
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM listings")
        rows = cursor.fetchall()

        for row in rows:
            print(f"ID: {row[0]}, Город: {row[1]}, Регион: {row[2]}, Описание: {row[3]}, Цена: {row[4]} руб., Контакт: {row[5]}, Фото: {row[6]}")
    except sqlite3.Error as e:
        print(f"Ошибка при получении данных: {e}")
    finally:
        connection.close()

# Добавление пользователя в таблицу user
def add_user_to_database(telegram_id, region):
    """Добавляет пользователя в таблицу user."""
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO user (telegram_id, region)
            VALUES (?, ?)
        """, (telegram_id, region))

        connection.commit()
        print(f"Пользователь с ID {telegram_id} добавлен в таблицу.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        connection.close()

# Получение региона пользователя из таблицы user
def get_user_region(telegram_id):
    """Получает регион пользователя по его telegram_id из таблицы user."""
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT region FROM user WHERE telegram_id = ?", (telegram_id,))
        region = cursor.fetchone()

        if region:
            return region[0]
        else:
            return None
    except sqlite3.Error as e:
        print(f"Ошибка при получении региона пользователя: {e}")
        return None
    finally:
        connection.close()

# Пример использования
if __name__ == "__main__":
    # Создание таблиц
    create_listings_table()
    create_user_table()

    # Добавление объявлений
    add_listing_to_database(
        city="Санкт-Петербург",
        region="Лененградская область",
        description="Просторная квартира с видом на Неву",
        price=60000,
        contact="+7 911 123-45-67",
        photo=r"C:\Users\Darkghost\Desktop\BD\photo1.jpg"
    )

    add_listing_to_database(
        city="Симферополь",
        region="Республика Крым",
        description="Однокомнатная квартира в спальном районе",
        price=40000,
        contact="+7 901 765-43-21",
        photo=rb"C:\Users\Darkghost\Desktop\BD\photo2.jpg"
    )

    add_listing_to_database(
        city="Армянск",
        region="Республика Крым",
        description="Уютная квартира",
        price=4000,
        contact="+7 901 765-43-21",
        photo=rb"C:\Users\Darkghost\Desktop\BD\photo2.jpg"
    )

    # Добавление пользователя
    add_user_to_database(telegram_id=7975249145, region="Республика Крым")

    # Получение региона пользователя
    region = get_user_region(telegram_id=7975249145)
    print(f"Регион пользователя: {region}")

    # Вывод всех объявлений
    print("\nСписок объявлений:")
    fetch_listings()