from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
