from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from AImodel.main import request
import asyncio, json

from Weather.Checker import get_weather

storage = MemoryStorage()

class Form(StatesGroup):
    city = State()

bot = Bot(token="")
dp = Dispatcher(storage = storage)

weather_button = KeyboardButton(text="Посмотреть погоду")
keyboard = ReplyKeyboardMarkup(keyboard=[[weather_button]], resize_keyboard=True)

@dp.message(Command("start"))
async def send_welcome(message: types.Message, state: FSMContext):
    username = message.from_user.username
    try:
        with open("Data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []
    except Exception as e:
        print(e)
        users = []

    is_true: bool = False
    for user in users:
        if user["username"] == username:
            is_true = True
            await message.answer(
                f"Hello, {message.from_user.first_name}!",
                reply_markup=keyboard
            )
            break
    if not is_true:
        await message.answer(f"Введите ваш город\n"
                             "Пример: Moscow")
        await state.set_state(Form.city)


@dp.message(lambda message: message.text == "Посмотреть погоду")
async def weather_handler(message: types.Message):
    data = None
    try:
        with open("Data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []
    except Exception as e:
        print(e)
        users = []
    for user in users:
        if user["username"] == message.from_user.username:
            data = await get_weather(user["city"])
            text = f"""
        Температура: {data[0]}°C\n
        Описание: {data[1]}\n
        Ветер: {data[2]} м/с\n
        Осадки: {data[3]} мм\n
            """
            break
    await message.answer(text)
    text = f"Привет, я-умный ассистент TonII\n\n Я помогу тебе выбрать одежду под погоду:\n\n "
    if "дождь" in data[1]:
        text += "На улице дождь! стоит взять зонт!\n"
    index = request(data[0], data[2], data[3]).item()
    if index < 2:
        text += "Стоило бы одеть теплую одежду\n На улице реально холодно..."
    elif index < 4:
        text += "Накинь на себя куртку, на улице прохладно\n"
    elif index < 6:
        text += "Думаю нормально будет накинуть небольшую кофточку\n"
    elif index < 8:
        text += "На улице нормально, футболочки хватит)"

    text += f"Наш железный робот оценивает погоду как: {index}"

    await message.answer(text)



@dp.message(Form.city)
async def process_name(message: types.Message, state: FSMContext):
    try:
        with open("Data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
    except Exception as e:
        print(e)
        users = []
    with open("Data/users.json", "w", encoding="utf-8") as f:
        users.append({
            "username": message.from_user.username,
            "city": message.text
        })
        json.dump(users, f)
        print("Json Dumped")
    await state.clear()
    await message.answer(f"Город добавлен\n"
                         "/start")


async def main():
    await dp.start_polling(bot)


