from aiogram import types, Router, F

from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile
from service.analysis_data import Punnett_tabla

user_private_router = Router()

# @user_private_router.message(CommandStart())
# async def command_start_handler(message):
#     ## Подключить InlineKeyboard
#     image = FSInputFile("photos\photo_2024-10-06_21-07-48.jpg")
#     await message.answer_photo(photo=image, caption="Привіт! \nВведи генотип особи чоловічої та жіночої статі: ")
    

@user_private_router.message()
async def send_answer(message: types.Message):
    with open("database\gen.txt", 'w') as f:
        user_message = message.text
        f.write(user_message)



