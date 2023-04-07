import aiogram
from aiogram.utils import executor
from aiogram import Dispatcher
from aiogram.types import Message
from settings import Telegram_token
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from database_connector import DatabaseConnector, uri

database = DatabaseConnector()
storage = MongoStorage(uri=uri)

bot = aiogram.Bot(token=Telegram_token)

dp = Dispatcher(bot, storage=storage)


class RegistrationForm(StatesGroup):
    name = State()
    username = State()
    password = State()


@dp.message_handler(commands=['start'])
async def register_start(message: Message):
    await message.answer("Введіть ваше ім'я?")
    await RegistrationForm.name.set()


@dp.message_handler(state=RegistrationForm.name)
async def register_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Введіть ваш логін?")
    await RegistrationForm.username.set()


@dp.message_handler(state=RegistrationForm.username)
async def register_email(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await message.answer("Введіть ваш пароль?")
    await RegistrationForm.password.set()


@dp.message_handler(state=RegistrationForm.password)
async def register_phone(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
        await message.answer(f"Дякуємо, {data['name']}! Ви зареєстровані на сайті")
    await state.finish()


executor.start_polling(dp)
