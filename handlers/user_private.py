import json
from aiogram import types, Router, F

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message

from service.analysis_data import Punnett_table

user_private_router = Router()

class Message_State(StatesGroup):
    # Реализовать State
    pass

@user_private_router.message()
async def command_help_handler(message: Message):
    if message.text == "/help":
        stickers = FSInputFile("photos\hi.webp")
        await message.answer_sticker(sticker=stickers, emoji="👋")
        await message.answer(text=("👋 Привіт! Цей бот допоможе проаналізувати генетичні питання 🧬, зокрема визначити можливі генотипи та ймовірність передачі ознак нащадкам 🌱 за допомогою таблиці Пеннета 📊. \nДізнавайся більше про генетику і свої спадкові можливості завдяки цім командам!\n" + " " * 20 + "=>    /start - запускає опитування"))

async def signs_message(message: Message):
    if message.text == "/start":
        image = FSInputFile() # Вставить фотографию для сообщения про ознаки
        await message.answer_photo(photo=image, caption="") # Дописать описание к ознакам + подключить клавиатуру

# Написать следуйщие этапы опроса


