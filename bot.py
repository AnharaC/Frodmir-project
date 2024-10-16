import asyncio
import os

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from dotenv import load_dotenv

load_dotenv()

from handlers.user_private import user_private_router

ALLOWED_UPDATES=['message, edites_message']

dp = Dispatcher()
bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp.include_router(user_private_router)

async def on_shutdown(bot):
    print("Ох бот решил упасть")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == "__main__":
    asyncio.run(main())
