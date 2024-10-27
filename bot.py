import asyncio
import os

from aiogram import Dispatcher, Bot, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv

load_dotenv()

from service.bot_cmds_list import private

from handlers.user_private import user_private_router

ALLOWED_UPDATES=['message, edites_message']

storage = MemoryStorage()
dp = Dispatcher()
bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp.include_router(user_private_router)

async def main():
    print("bot started")

    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == "__main__":
    asyncio.run(main())
