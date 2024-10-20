from filters.chat_types import ChatTypeFilter
from aiogram import Router

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))
