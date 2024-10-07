from aiogram import types, Router
from aiogram.filters import CommandStart

user_private_router = Router()

@user_private_router.message(CommandStart())
async def command_start_handler(message):
    ## Подключить InlineKeyboard
    await message.answer_photo(photo="https://img2.joyreactor.cc/pics/post/furry-%D1%84%D1%8D%D0%BD%D0%B4%D0%BE%D0%BC%D1%8B-windu_utom-8362527.jpeg", caption="Hi")