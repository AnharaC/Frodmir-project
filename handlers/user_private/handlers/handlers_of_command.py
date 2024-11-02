from aiogram import types, F
import logging
import os

from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.types import Message, FSInputFile

from keyboard.InlineKeyboard import get_callback_btns
from service.survey_manager import get_survey_filename, get_survey_result

from .first_survey_handlers import *
from .second_survey_handlers import *
from .history_handler import *

from ..MessageState import MessageState
from ..router import user_private_router

from middleware.MessageMiddleware import UserMessageMiddleware
from middleware.CallbackMiddleware import CallbackMiddleware

user_private_router.message.middleware(UserMessageMiddleware())
user_private_router.callback_query.middleware(CallbackMiddleware())

logging.basicConfig(level=logging.INFO)

# Handler що не буде давати вводити команди під час опитування
@user_private_router.message(
        StateFilter(MessageState.quest_1, MessageState.quest_2, MessageState.quest_3, MessageState.st_quest_2, MessageState.st_quest_3, MessageState.stage_1, MessageState.stage_2), 
        Command('help', 'start', 'about', 'survey', 'history'))
async def block_commands(message: Message, state: FSMContext):
    current_state = await state.get_state()
    gif = os.path.join('assets', 'image', 'bot eto da.webm')
    await message.answer_sticker(sticker=FSInputFile(gif), emoji="✋")
    await message.answer("Опа, а низя низя!! Доки не скасуешь опитування, або не пройдешь низя низя")


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
