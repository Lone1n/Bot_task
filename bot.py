import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio

BOT_TOKEN = '7122336874:AAGNB4TDa-626Ly72VKD1xg-GCzl56MjQnc'

API_KEY = '837d4d6e68e73e1642f9c628b60d1d6d'

API_URL = f"http://api.currencylayer.com/live?access_key={API_KEY}&currencies=USD,RUB"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    waiting_for_name = State()

@dp.message(Command("start"))
async def send_welcome(message: Message, state: FSMContext):
    await message.answer("Добрый день. Как вас зовут?")
    await state.set_state(Form.waiting_for_name)

@dp.message(F.text, Form.waiting_for_name)
async def ask_name(message: Message, state: FSMContext):
    name = message.text
    try:

        response = requests.get(API_URL)
        data = response.json()
        usd_to_rub = data['quotes']['USDRUB']
        
        await message.answer(f"Рад знакомству, {name}! Курс доллара сегодня {usd_to_rub:.2f}₽")
    except Exception as e:
        await message.answer(f"Не удалось получить курс доллара. Ошибка: {e}")
    await state.clear()

@dp.message(F.text == "Старт")
async def handle_start_button(message: Message, state: FSMContext):
    await send_welcome(message, state)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
