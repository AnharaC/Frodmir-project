from datetime import datetime

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Callable, Dict, Any, Awaitable

from service.save_data import save_user_data


class UserMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)  # Перевірка на те чи є в data - user

        user_id = user.id
        user_name = user.username
        user_message = data.get("event_update").message.text
        processing_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_data = {
            "Date/time": f"{processing_time}",
            "ID": f"{user_id}",
            "User_Name": f"{user_name}",
            "User_Message": f"{user_message}",
        }

        response = await handler(event, data)

        save_user_data(user_id, log_data)

        return response
