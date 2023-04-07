import aiogram
from aiogram.utils import executor
from aiogram import Dispatcher
from aiogram.types import Message
from settings import Telegram_token
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from database_connector import DatabaseConnector, uri
import bcrypt

database = DatabaseConnector()
storage = MongoStorage(uri=uri)

bot = aiogram.Bot(token=Telegram_token)

dp = Dispatcher(bot, storage=storage)


class RegistrationForm(StatesGroup):
    name = State()
    username = State()
    password = State()
    confirm_password = State()


@dp.message_handler(commands=['start'])
async def register_start(message: Message):
    await message.answer("Почнемо реєстрацію на сайті. Введіть ваше ім'я?")
    await RegistrationForm.name.set()


@dp.message_handler(state=RegistrationForm.name)
async def register_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Введіть ваш логін?")
    await RegistrationForm.username.set()


@dp.message_handler(state=RegistrationForm.username)
async def register_username(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await message.answer("Введіть ваш пароль? Після того як ви введете ми його видалимо з чату")
    await RegistrationForm.password.set()


@dp.message_handler(state=RegistrationForm.password)
async def register_password(message: Message, state: FSMContext):
    async with state.proxy() as data:
        hashed_password = bcrypt.hashpw(message.text.encode(), bcrypt.gensalt())
        data['hashed_password'] = hashed_password
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(chat_id=message.chat.id, text="Введіть пароль ще раз для підтвердження. "
                                                         "Після того як ви введете ми його видалимо з чату")
    await RegistrationForm.confirm_password.set()


@dp.message_handler(state=RegistrationForm.confirm_password)
async def confirm_password(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if bcrypt.checkpw(message.text.encode(), data['hashed_password']):
            database.users.insert_one(prepare_user_data(data, message))
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await message.answer(f"Дякуємо, {data['name']}! Ви зареєстровані на сайті")
            await state.finish()
        else:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await message.answer("Неправильний пароль. Спробуйте ще раз.")
            await message.answer("Введіть ваш пароль? Після того як ви введете ми його видалимо з чату")
            await RegistrationForm.password.set()


def prepare_user_data(data, message):
    user_data = {
        'name': data['name'],
        'username': data['username'],
        'password': data['hashed_password'],
        'telegram_id': message.from_user.id,
        'first_name': message.from_user.first_name
    }

    return user_data


executor.start_polling(dp)
