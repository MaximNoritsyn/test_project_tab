import os
from dotenv import load_dotenv

load_dotenv()

Telegram_token = os.environ.get('Telegram_token')
Telegram_bot_name = os.environ.get('Telegram_bot_name')

MONGODB_HOST = os.environ.get('MONGODB_HOST')
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME')

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = 'HS256'
