import json
from datetime import datetime

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Callable, Dict, Any, Awaitable

class UserMessageHandler(BaseMiddleware):
    async def __call__(self, 
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event:  TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data) # Перевірка на те чи є в data - user

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

        if 'state' in data and data['state']: #Провірка чи є state в data
            state_data = await data['state'].get_data() # Достаємо якщо state є
            if 'quests' in state_data: # Перевірка чи є данні в quests
                log_data['quests'] = state_data['quests'] # Якщо так то додаються до log_data
            else: # Якщо нема то створення пустой структурі
                log_data['quests'] = {
                    "start_quest": {
                        "result_quest1": None,
                        "result_quest2": None,
                        "result_quest3": None
                    },
                    "gen": None
                }

        try: # Перевірка на те чи існує логі с конкретним користувачом
            with open(f"data_logs/server_logs/user_{user_id}.json", "r", encoding="utf-8") as file:
                existing_data = json.load(file)
        except (FileNotFoundError):
            existing_data = []

        existing_data.append(log_data) # Нова запись додається до все існуючих
            
        with open(f"data_logs/server_logs/user_{user_id}.json", "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4)

        return response

