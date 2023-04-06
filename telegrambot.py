import aiogram
from aiogram.utils import executor
from settings import Telegram_token

bot = aiogram.Bot(token=Telegram_token)

dp = aiogram.Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: aiogram.types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Hello world"
    )


executor.start_polling(dp)
