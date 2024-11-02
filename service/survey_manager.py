import json
import os

def get_next_survey_id(user_id: int):
    directory = f"data/user_history/user_{user_id}"
    os.makedirs(directory, exist_ok=True)
    existing_ids = []

    for filename in os.listdir(directory):
        if filename.startswith(f"survey_user_{user_id}_"):
            survey_id = int(filename.split('_')[-1].split('.')[0])
            existing_ids.append(survey_id)

    return max(existing_ids, default=0) + 1


def save_survey(user_id: int, results):
    survey_id = get_next_survey_id(user_id)
    directory = f"data/user_history/user_{user_id}"

    os.makedirs(directory, exist_ok=True)

    data_to_save = {
        "user_id": user_id,
        "survey_id": survey_id,
        "results": results
    }

    with open(f"{directory}/survey_user_{user_id}_{survey_id}.json", 'w') as file:
        json.dump(data_to_save, file, indent=4)

    print(f"For user_{user_id}, result saved in survey_user_{user_id}_{survey_id}.json")


def get_survey_filename(user_id: int):
    directory = f"data/user_history/user_{user_id}"
    survey_filenames = []

    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.startswith(f"survey_user_{user_id}"):
                survey_number = filename.split('_')[-1][:-5]
                pretty_name = f"Опитування №{survey_number}"
                survey_filenames.append(pretty_name)

    return survey_filenames


def get_survey_result(user_id: int, survey_id: int):
    directory = f"data/user_history/user_{user_id}"
    file_path = f"{directory}/survey_user_{user_id}_{survey_id}.json"

    if os.path.exists(file_path): # Перевірка на те чи існує файл
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        print("Упс щось то не так")
        return None

