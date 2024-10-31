import json

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Callable, Dict, Any, Awaitable

from service.save_data import save_user_data 

class CallbackMiddleware(BaseMiddleware):
    async def __call__(self, 
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event:  TelegramObject,
                       data: Dict[str, Any]) -> Any:

        user_id = data.get("event_from_user").id
        log_data = {}
        
        response = await handler(event, data)
        state_data = await data['state'].get_data() # Достаємо якщо state є
        
        log_data['quests'] = state_data.get('quests', {
            "start_quest": {
                "result_quest1": None,
                "result_quest2": None,
                "result_quest3": None
            },
            "gen": None
        })
        
        file_path = f"data/user_server/user_{user_id}.json"
        save_user_data(user_id, log_data, file_path)

        return response