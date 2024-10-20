from aiogram import types, Router, F

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.types import FSInputFile, Message
from aiogram.utils.deep_linking import decode_payload

from keyboard.InlineKeyboard import get_callback_btns
from service.analysis_data import Punnett_table, analis
from filters.chat_types import ChatTypeFilter

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))


class Message_State(StatesGroup):
    quest_1 = State()
    quest_2 = State()
    quest_3 = State()
    # start_easy_survey = State()
    # start_detailed_survey = State()
    analis_answer = State()
    # get_result = State()

open("database/temp_data.json", 'w').close()

@user_private_router.message(or_f(Command("help", "start"), CommandStart(deep_link=True)))
async def command_help_handler(message: Message):
    stickers = FSInputFile("photos\hi.webp")


    await message.answer_sticker(sticker=stickers, emoji="👋")
    await message.answer(text=(
        "👋 Привіт! Цей бот допоможе проаналізувати генетичні питання 🧬, "
        "зокрема визначити можливі генотипи та ймовірність передачі ознак "
        "нащадкам 🌱 за допомогою таблиці Пеннета 📊.\n\n"
        "Дізнавайся більше про генетику і свої спадкові можливості завдяки цім командам:\n"
        "\t\t\t=> /about - докладніше про бота\n"
        "\t\t\t=> /survey - запускає опитування\n"
        "\t\t\t=> /history - історія ваших подій"
    ))


@user_private_router.message(Command("about"))
async def command_about_handler(message: Message):
    videos = FSInputFile("photos\ой сало сало сало українське сало «high resolution».mp4")

    await message.answer_video(
    video=videos, 
    caption=(
        "👋 Привіт! Раді вітати тебе в боті, який допоможе заглибитись у світ генетики 🧬. "
        "Наш бот здатний відповісти на різні генетичні питання та проаналізувати твої відповіді, "
        "щоб визначити можливі генотипи 🧑‍🔬 і передбачити ймовірність передачі спадкових ознак 🌱.\n\n"
        "За допомогою таблиці Пеннета 📊 ти дізнаєшся, як певні ознаки можуть проявитися "
        "у твоїх майбутніх нащадків 🤱. Це ідеальна можливість не лише розібратися в своїй генетиці, "
        "але й поглибити свої знання про основи спадковості 🧠."
        " " * 20 +
        " Натискай => /survey - щоб розпочати опитування та дізнатися більше про свої спадкові можливості! "
        "Бот задасть кілька простих запитань, а ти отримаєш результат у вигляді генетичного прогнозу 🔮."
        )
    )  


# @user_private_router.message(StateFilter(None), or_f(CommandStart(), (F.text.lower() == "старт")))
# async def signs_message(message: Message):
#     if message.text == "/start":
#         image = FSInputFile("photos\photo_2024-09-01_09-52-18.jpg")
#         await message.answer_photo(photo=image, caption="Оберіть тип опитування",
#                                    reply_markup=get_callback_btns(btns={
#                                        "Легке опитування": "eaysy_survey",
#                                        "Детальне опитування": "detailed_survey",
#                                    }))


@user_private_router.message(F.text.lower() == "ти бачишь мене?")
async def see_me(message: Message):
    video = FSInputFile("photos\IMG_5115.MP4")
    await message.answer_video(video=video)


@user_private_router.message(StateFilter(None), or_f(Command("/survey"), (F.text.lower() == "опитування")))
async def command_start_handler(message: Message, state: FSMContext):
    image = FSInputFile("photos\photo_2024-10-16_08-56-42.jpg")

    await state.set_state(Message_State.quest_1)

    await message.answer_photo(photo=image, caption="За якими ознаками ви хотіл би розпочати?",
                                            reply_markup=get_callback_btns(btns={
                                                "Колір очей": "type_of_color_eye",
                                                "Група крові": "type_of_blood",
                                            }))


@user_private_router.callback_query(F.text.lower() == "доступно")
async def detailed_survey(callback: types.CallbackQuery):
    video = FSInputFile("photos\RPReplay_Final1705860476.mp4")
    await callback.message.answer_video(video=video, caption="Ой ой ой а це ще не доступно, соси бібу")


## Все про очи
@user_private_router.callback_query(Message_State.quest_1, F.data.startswith('type_of_color_eye'))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    gif = FSInputFile('photos\аллах-халяль.gif')

    await state.set_state(Message_State.quest_2)

    await callback.message.answer_animation(animation=gif,
                                                reply_markup=get_callback_btns(btns={
                                                    "Блакитні": "blue",
                                                    "Карі": "kari",
                                                    "Зелено/Світло карі": "green/light_brown",
                                                }))
        
        
## Все про карій
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith('kari'))
async def second_quest(callback: types.CallbackQuery, state: FSMContext):
    image = FSInputFile('photos/furry-фэндомы-furry-m-8352840.jpeg')

    await state.set_state(Message_State.analis_answer)

    await callback.message.answer_photo(photo=image,
                                            caption="Чи були в одно з батькві, братів/сестер блакитні очі?",
                                            reply_markup=get_callback_btns(btns={
                                                "Так": "final_yes_kari",
                                                "Ні": "final_no_kari",
                                            }))


@user_private_router.callback_query(Message_State.analis_answer, F.data.startswith('final_yes_kari'))
async def analis_answer(callback: types.CallbackQuery, state: FSMContext):

    data = {
    'gen': "Aa, aa"
    }

    analis(data=data)

    male_genotype, children_genotypes, percentage, female_genotype = Punnett_table()
    await callback.message.answer(text=f"{male_genotype}; \n{female_genotype}; \n{children_genotypes}; \n{percentage}")

    await state.clear()


@user_private_router.callback_query(Message_State.analis_answer, F.data.startswith('final_no_kari'))
async def analis_answer_no(callback: types.CallbackQuery, state: FSMContext):

    data = {
    'gen': "AA, Aa"
    }

    analis(data=data)
        
    male_genotype, children_genotypes, percentage, female_genotype = Punnett_table()
    await callback.message.answer(text=f"{male_genotype}; \n{female_genotype}; \n{children_genotypes}; \n{percentage}")
        
    await state.clear()


## Все про блакитний
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith('blue'))
async def analis_answer_blue(callback: types.CallbackQuery, state: FSMContext):

    data = {
        'gen': 'aa, aA'
    }

    analis(data=data)

    male_genotype, children_genotypes, percentage, female_genotype = Punnett_table()
    await callback.message.answer(text=f"{male_genotype}; \n{female_genotype}; \n{children_genotypes}; \n{percentage}")
        
    await state.clear()


## Все про світло зелено блакитний
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith('green/light_brown'))
async def analis_answer_green_light_brown(callback: types.CallbackQuery, state: FSMContext):

    data = {
        'gen': 'AA, aa'
    }

    analis(data=data)

    male_genotype, children_genotypes, percentage, female_genotype = Punnett_table()
    await callback.message.answer(text=f"{male_genotype}; \n{female_genotype}; \n{children_genotypes}; \n{percentage}")
        
    await state.clear()


## Все про групу крові
@user_private_router.callback_query(Message_State.quest_1, F.data.startswith('type_of_blood'))
async def eaysy_survey(callback: types.CallbackQuery, state: FSMContext):
    image = FSInputFile('photos\photo_2024-10-19_10-02-38.jpg')

    await state.set_state(Message_State.quest_2)
    
    await callback.message.answer_photo(photo=image, caption="Яка ваша група крові?",
                                            reply_markup=get_callback_btns(btns={
                                                "I(O)": "first_blood",
                                                "II(A)": "second_blood",
                                                "III(B)": "third_blood",
                                                "IV(AB)": "fourth_blood",
                                            }))


## Перша група крові
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith("first_blood"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    gif = FSInputFile('photos\komaru-комару.gif')

    data = {
        'gen': 'OO, Aa'
    }

    analis(data=data)

    male_genotype, children_genotypes, percentage, female_genotype = Punnett_table()
    await callback.message.answer(text=f"{male_genotype}; \n{female_genotype}; \n{children_genotypes}; \n{percentage}")
        
    await state.clear()


## Друга група крові
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith("second_blood"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    video = FSInputFile('photos\эпик фейл.mp4')

    await state.set_state(Message_State.analis_answer)
    
    await callback.message.answer_video(video=video,
                                            caption="Чи була в одного з батьків, братів\сестер I(О) група крові?",
                                            reply_markup=get_callback_btns(btns={
                                                "Так": "final_yes_blood",
                                                "Ні": "final_no_blood",
                                            }))


@user_private_router.callback_query(Message_State.analis_answer, F.data.startswith('final_yes_blood'))
async def analis_answer(callback: types.CallbackQuery, state: FSMContext):

    data = {
    'gen': "AO, aa"
    }

    analis(data=data)

    male_genotype, children_genotypes, percentage, female_genotype = Punnett_table()
    await callback.message.answer(text=f"{male_genotype}; \n{female_genotype}; \n{children_genotypes}; \n{percentage}")
        
    await state.clear()


@user_private_router.callback_query(Message_State.analis_answer, F.data.startswith('final_no_blood'))
async def analis_answer_no(callback: types.CallbackQuery, state: FSMContext):

    data = {
    'gen': "AA, aA"
    }

    analis(data=data)
        
    male_genotype, children_genotypes, percentage, female_genotype = Punnett_table()
    await callback.message.answer(text=f"{male_genotype}; \n{female_genotype}; \n{children_genotypes}; \n{percentage}")
        
    await state.clear()


## Терться група крові
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith("third_blood"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    image = FSInputFile('photos\wqdasd.jpg')

    await state.set_state(Message_State.analis_answer)
    
    await callback.message.answer_photo(photo=image,
                                            caption="Чи була в одного з батьків, братів\сестер I(О) група крові?",
                                            reply_markup=get_callback_btns(btns={
                                                "Так": "final_yes_blood",
                                                "Ні": "final_no_blood",
                                            }))


@user_private_router.callback_query(Message_State.analis_answer, F.data.startswith('final_yes_blood'))
async def analis_answer(callback: types.CallbackQuery, state: FSMContext):

    data = {
    'gen': "BB, OA"
    }

    analis(data=data)

    male_genotype, children_genotypes, percentage, female_genotype = Punnett_table()
    await callback.message.answer(text=f"{male_genotype}; \n{female_genotype}; \n{children_genotypes}; \n{percentage}")
        
    await state.clear()


@user_private_router.callback_query(Message_State.analis_answer, F.data.startswith('final_no_blood'))
async def analis_answer_no(callback: types.CallbackQuery, state: FSMContext):

    data = {
    'gen': "BO, AO"
    }

    analis(data=data)
        
    male_genotype, children_genotypes, percentage, female_genotype = Punnett_table()
    await callback.message.answer(text=f"{male_genotype}; \n{female_genotype}; \n{children_genotypes}; \n{percentage}")
        
    await state.clear()

## Четверта група крові
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith("fourth_blood"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    gif = FSInputFile('photos\image0-156-1-1.gif')

    data = {
        'gen': 'AB, OO'
    }

    analis(data=data)

    male_genotype, children_genotypes, percentage, female_genotype = Punnett_table()
    await callback.message.answer(text=f"{male_genotype}; \n{female_genotype}; \n{children_genotypes}; \n{percentage}")
        
    await state.clear()


# print("Provekra 1")
# @user_private_router.message(Message_State.get_result)
# async def execute_table(message: types.Message, state: FSMContext):
#     print("Provekra 2")
#     male_genotype, children_genotypes, percentage, female_genotype = Punnett_table()
#     print("Provekra 3")
#     await message.answer(text=f"{male_genotype}; \n{female_genotype}; \n{children_genotypes}; \n{percentage}")
    
#     await state.clear()






