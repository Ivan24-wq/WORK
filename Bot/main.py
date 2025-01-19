import sqlite3

def add_listing_to_database(city, description, price, contact):
    """Добавляет запись в таблицу listings."""
    try:
        # Подключение к базе данных
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        # Добавление записи
        cursor.execute("""
            INSERT INTO listings (city, description, price, contact)
            VALUES (?, ?, ?, ?)
        """, (city, description, price, contact))

        # Сохранение изменений
        connection.commit()
        print(f"Объявление добавлено: {city}, {description}, {price} руб., {contact}")

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении объявления: {e}")
    finally:
        # Закрытие соединения
        connection.close()


# Пример добавления данных
add_listing_to_database(
    city="Санкт-Петербург",
    description="Просторная квартира с видом на Неву",
    price=60000,
    contact="+7 911 123-45-67"
)

add_listing_to_database(
    city="Москва",
    description="Однокомнатная квартира в спальном районе",
    price=40000,
    contact="+7 901 765-43-21"
)
