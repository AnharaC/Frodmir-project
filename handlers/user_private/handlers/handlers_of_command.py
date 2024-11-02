from aiogram import types, F
import os

from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.types import Message, FSInputFile

from keyboard.InlineKeyboard import get_callback_btns
from service.survey_manager import get_survey_filename, get_survey_result

from .first_survey_handlers import *
from .second_survey_handlers import *

from ..MessageState import MessageState
from ..router import user_private_router

from middleware.MessageMiddleware import UserMessageMiddleware
from middleware.CallbackMiddleware import CallbackMiddleware

user_private_router.message.middleware(UserMessageMiddleware())
user_private_router.callback_query.middleware(CallbackMiddleware())



## Handlers відповідаючи за start
@user_private_router.message(or_f(Command("start"), CommandStart(deep_link=True)))
async def command_start_handler(message: Message):
    stickers = os.path.join('assets', 'stickers', 'hi.webp')

    await message.answer_sticker(sticker=FSInputFile(stickers), emoji="👋")
    await message.answer(text=(
        "👋 Привіт! Цей бот допоможе проаналізувати генетичні питання 🧬. "
        "Ви зможете визначити можливі генотипи і ймовірність передачі ознак "
        "нащадкам 🌱 за допомогою таблиці Пеннета 📊.\n\n"
        "Що вміє цей бот:\n"
        "🧬 Аналіз генетичних комбінацій\n"
        "📊 Визначення ймовірності передачі ознак\n"
        "🌱 Дослідження генетичних варіацій\n\n"
        "Команди для початку роботи:\n"
        "\t\t\t=> /help - список всіх команд бота\n"
        "\t\t\t=> /about - дізнайтесь більше про роботу бота"
    ))

## Handlers відповідаючи за help
@user_private_router.message(Command("help"))
async def command_help_handler(message: Message):
    stickers = os.path.join('assets', 'stickers', 'owo.webp')

    await message.answer_sticker(sticker=FSInputFile(stickers), emoji="👀")
    await message.answer(text=(
        "📋 Ось команди для роботи з ботом:\n\n"
        "💡 /about - докладніше про бота\n"
        "📝 /survey - запуск опитування для глибшого аналізу\n"
        "📜 /history - перегляд історії ваших запитів"
    ))

## Handlers відповідаючи за about
@user_private_router.message(Command("about"))
async def command_about_handler(message: Message):
    image = os.path.join('assets', 'image', 'photo_2024-10-18_16-02-20.jpg')

    await message.answer_photo(
    photo=FSInputFile(image),
    caption=(
        "👋 Привіт! Раді вітати тебе в боті, який допоможе заглибитись у світ генетики 🧬. "
        "Наш бот здатний відповісти на різні генетичні питання та проаналізувати твої відповіді, "
        "щоб визначити можливі генотипи 🧑‍🔬 і передбачити ймовірність передачі спадкових ознак 🌱.\n\n\t\t\t"
        "За допомогою таблиці Пеннета 📊 ти дізнаєшся, як певні ознаки можуть проявитися "
        "у твоїх майбутніх нащадків 🤱. Це ідеальна можливість не лише розібратися в своїй генетиці, "
        "але й поглибити свої знання про основи спадковості 🧠."
        "\n\n\t\t\t<strong>Натискай => /survey</strong> - щоб розпочати опитування та дізнатися більше про свої спадкові можливості! "
        "Бот задасть кілька простих запитань, а ти отримаєш результат у вигляді генетичного прогнозу 🔮."
        )
    )

## Handlers відповідаючи за clear(тимчасова команда)
@user_private_router.message(Command("clear"))
async def command_clear_handler(message: Message, state: FSMContext):
    image = os.path.join('assets', 'image', 'photo_2024-10-30_15-01-47.jpg')

    await state.clear()
    await message.answer_photo(photo=FSInputFile(image), caption="Clear!!")

## Handlers відповідаючи за history
@user_private_router.message(Command("history"))
async def detailed_survey(message: Message, state: FSMContext):
    user_id = message.from_user.id
    photo = os.path.join('assets', 'image', 'photo_2024-10-26_13-10-32.jpg')

    survey_filenames = get_survey_filename(user_id=user_id)
    history_message = "📜 Історія опитуваннь:\n\n" + "\n".join([f"✅ {filename}" for filename in survey_filenames])
    history_message += "\n\nНапишіть який з цих результатів опитуваннь ви хотіли би переглянути (Введіть номер опитування): "
    await message.answer(history_message)

    await state.set_state(MessageState.waiting_for_survey_selection)
    await state.update_data(survey_filenames=survey_filenames)

@user_private_router.message(MessageState.waiting_for_survey_selection)
async def proc_survey_selection(message: Message, state: FSMContext):
    user_id = message.from_user.id
    selected_survey = message.text.strip()

    data = await state.get_data()
    survey_filenames = data.get("survey_filenames") # Забираємо список пройдених опитувань
    
    survey_id = int(selected_survey.split('_')[-1].split('.')[0]) # Забираємо номер опитування
    survey_data = get_survey_result(user_id=user_id, survey_id=survey_id)
    
    if survey_data:
        results = survey_data['results']
        results_message = "\n".join(
            [f"\t\t\t\t📌 Питання {question_id}: {response if response is not None else 'Не відповіли'}"
             for question_id, response in results.items()]) # Створюємо строку з результатами опитування використовуючи result.items() для перебору та форматування кожного питання та його відповіді
        
        await message.answer(text=(
            f"📄 Деталі опитування №{survey_data['survey_id']}:\n"
            f"👤 ID користувача: {survey_data['user_id']}\n"
            f"📝 Результати:\n{results_message}"
        ))
    else:
        await message.answer("Не вдалося отримати данні. Спробуйте пізніше")


## Handlers відповідаючи за survey
@user_private_router.message(StateFilter(None), or_f(Command("survey"), (F.text.lower() == "опитування")))
async def command_start_handler(message: Message, state: FSMContext):
    image = os.path.join('assets', 'image', 'photo_2024-10-16_08-56-42.jpg')

    user_data = await state.get_data()
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)

    await state.set_state(MessageState.quest_1)
    await state.update_data(quests={
        "start_quest": {
            "survey_number": None,
            "result_quest1": None,
            "result_quest2": None,
            "result_quest3": None
        },
        "gen": {
            1: None,
            2: None
        }
    })

    await message.answer_photo(photo=FSInputFile(image), caption="Оберіть ознаку за якою ви пройдете два опитування (Від себе і свого партнера): ",
                                            reply_markup=get_callback_btns(btns={
                                                "Колір очей": "type_of_color_eye_first",
                                                "Група крові": "type_of_blood_first",
                                                "Назад": "return",
                                                "Відмінити": "cancel",
                                            }))
    

## Handlers які відповідальні за "Назад" та "Відмінити"

# Handlers відповідаючи за cancel
@user_private_router.callback_query(StateFilter("*"), F.data.startswith("cancel"))
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    curent_state = await state.get_state()
    if curent_state is None:
        return
    
    user_data = await state.get_data()
    quests = user_data.get("quests", {})
    survey_number = (quests.get("start_quest", {}).get("survey_number") or 0) - 1

    if survey_number < 0:
        survey_number = 0
    
    quests['start_quest']['survey_number'] = survey_number
    await state.update_data(quests=quests)

    await state.clear()
    await callback.message.answer("Опитування була відмінено")

## Handlers відповідаючи за back
@user_private_router.callback_query(StateFilter("*"), F.data.startswith("return"))
async def back_step_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    user_data = await state.get_data()
    quests = user_data.get('quests', {})

    if current_state == MessageState.quest_1:
        sticker = os.path.join('assets', 'image', 'svabodin.webm')
        await callback.message.answer_sticker(sticker=FSInputFile(sticker), emoji="🤬")
        await callback.message.answer("А все! Нема куди повертатися, анлак бро", reply_markup=types.ReplyKeyboardRemove())
        return

    previous_question = quests['start_quest'].get('result_quest1', None)

    await callback.message.answer("Ви повернулись на попередне питання. Зачекайте поки повториться питання")

    if previous_question == 'type_of_color_eye_first':
        if current_state == MessageState.quest_2:
            await command_start_handler(callback.message, state)

        elif current_state == MessageState.quest_3:
            await second_quest_eye(callback, state)

        elif current_state == MessageState.stage_1:
            await third_quest_eye(callback, state)

    elif previous_question == 'type_of_blood_first':
        if current_state == MessageState.quest_2:
            await command_start_handler(callback.message, state)

        elif current_state == MessageState.quest_3:
            await second_quest_blood(callback, state)

        elif current_state == MessageState.stage_1:
            await third_quest_blood(callback, state)


    elif previous_question == 'type_of_color_eye_second':
        if current_state == MessageState.st_quest_2:
            await command_start_handler(callback.message, state)

        elif current_state == MessageState.st_quest_3:
            await second_questionare(callback, state)

        elif current_state == MessageState.stage_2:
            await third_quest_eye(callback, state)

    elif previous_question == 'type_of_blood_second':
        if current_state == MessageState.st_quest_2:
            await command_start_handler(callback.message, state)

        elif current_state == MessageState.st_quest_3:
            await second_quest_blood(callback, state)

        elif current_state == MessageState.stage_2:
            await third_quest_blood(callback, state)
        
    previous = None
    for step in MessageState.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            return

        previous = step
