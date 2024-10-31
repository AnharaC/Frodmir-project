import json
from typing import Any, Dict

def save_user_data(user_id: int, log_data: Dict[str, Any], file_path: str) -> None:
    existing_data = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        pass

    existing_data.append(log_data)

    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4)

# def save_result_data()



