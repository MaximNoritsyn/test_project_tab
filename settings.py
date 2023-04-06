import os
from dotenv import load_dotenv

load_dotenv()

Telegram_token = os.environ.get('Telegram_token')
Telegram_bot_name = os.environ.get('Telegram_bot_name')