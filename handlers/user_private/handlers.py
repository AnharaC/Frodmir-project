from aiogram import types, F
import os

from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.types import Message, FSInputFile

from keyboard.InlineKeyboard import get_callback_btns
from service.analysis_data import Punnett_table
from .MessageState import Message_State
from .router import user_private_router

@user_private_router.message(or_f(Command("help", "start"), CommandStart(deep_link=True)))
async def command_help_handler(message: Message):
    stickers = os.path.join('assets', 'image', 'hi.webp')

    await message.answer_sticker(sticker=FSInputFile(stickers), emoji="👋")
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
    photo = os.path.join('assets', 'image', 'photo_2024-10-18_16-02-20.jpg')

    await message.answer_photo(
    photo=FSInputFile(photo), 
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


@user_private_router.message(F.text.lower() == "ти бачишь мене?")
async def see_me(message: Message):
    video = os.path.join('assets', 'video', 'ssstik.io_@yuipaws_1728557809636.mp4')
    await message.answer_video(video=FSInputFile(video))


@user_private_router.message(StateFilter(None), or_f(Command("survey"), (F.text.lower() == "опитування")))
async def command_start_handler(message: Message, state: FSMContext):
    image = os.path.join('assets', 'image', 'photo_2024-10-16_08-56-42.jpg')

    await state.set_state(Message_State.quest_1)
    await state.update_data(quests={
        "start_quest": {
            "result_quest1": None,
            "result_quest2": None,
            "result_quest3": None
        },
        "gen": None
    })
    await message.answer_photo(photo=FSInputFile(image), caption="За якими ознаками ви хотіл би розпочати?",
                                            reply_markup=get_callback_btns(btns={
                                                "Колір очей": "type_of_color_eye",
                                                "Група крові": "type_of_blood",
                                            }))


@user_private_router.callback_query(F.text.lower() == "доступно")
async def detailed_survey(callback: types.CallbackQuery):
    video = os.path.join('assets', 'video', 'RPReplay_Final1705860476.mp4')
    await callback.message.answer_video(video=FSInputFile(video), caption="Ой ой ой а це ще не доступно, соси бібу")


## Все про очи
@user_private_router.callback_query(Message_State.quest_1, F.data.startswith('type_of_color_eye'))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    gif = os.path.join('assets', 'image', 'аллах-халяль.gif')

    await state.set_state(Message_State.quest_2)
    
    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest1'] = callback.data

    await state.update_data(quests=quests)

    await callback.message.answer_animation(animation=FSInputFile(gif),
                                                reply_markup=get_callback_btns(btns={
                                                    "Блакитні": "blue",
                                                    "Карі": "kari",
                                                    "Зелено/Світло карі": "green/light_brown",
                                                }))
        
        
## Все про карій
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith('kari'))
async def second_quest(callback: types.CallbackQuery, state: FSMContext):
    image = os.path.join('assets', 'image', 'furry-фэндомы-furry-m-8352840.jpeg')

    await state.set_state(Message_State.analis_answer)

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = callback.data

    await state.update_data(quests=quests)

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чи були в одно з батькві, братів/сестер блакитні очі?",
                                            reply_markup=get_callback_btns(btns={
                                                "Так": "final_yes_kari",
                                                "Ні": "final_no_kari",
                                            }))


@user_private_router.callback_query(Message_State.analis_answer, F.data.startswith('final_yes_kari'))
async def analis_answer(callback: types.CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Так]:"
    quests['gen'] = "[Aa,aa]"

    await state.update_data(quests=quests)

    await state.clear()
        

@user_private_router.callback_query(Message_State.analis_answer, F.data.startswith('final_no_kari'))
async def analis_answer_no(callback: types.CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Ні]:"
    quests['gen'] = "[AA,Aa]"

    await state.update_data(quests=quests)
           
    await state.clear()


## Все про блакитний
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith('blue'))
async def analis_answer_blue(callback: types.CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    quests = user_data['quests']

    quests['start_quest']['result_quest2'] = "[Блакитні]:"
    quests['gen'] = ['aa', 'aA']

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes = user_data['quests']['gen']

    await Punnett_table(callback, genotypes)

    await state.clear()


## Все про світло зелено блакитний
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith('green/light_brown'))
async def analis_answer_green_light_brown(callback: types.CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = "[зелено-блакитні]:"
    quests['gen'] = "[AA,aa]"

    await state.update_data(quests=quests)

    await state.clear()


## Все про групу крові
@user_private_router.callback_query(Message_State.quest_1, F.data.startswith('type_of_blood'))
async def eaysy_survey(callback: types.CallbackQuery, state: FSMContext):
    image = os.path.join('assets', 'image', 'photo_2024-10-19_10-02-38.jpg')

    await state.set_state(Message_State.quest_2)
    
    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest1'] = callback.data

    await state.update_data(quests=quests)
    
    await callback.message.answer_photo(photo=FSInputFile(image), caption="Яка ваша група крові?",
                                            reply_markup=get_callback_btns(btns={
                                                "I(O)": "first_blood",
                                                "II(A)": "second_blood",
                                                "III(B)": "third_blood",
                                                "IV(AB)": "fourth_blood",
                                            }))


## Перша група крові
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith("first_blood"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    # gif = os.path.join('assets', 'image', 'komaru-комару.gif')

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = "I(O)"
    quests['gen'] = "[OO,Aa]"

    await state.update_data(quests=quests)

    await state.clear()


## Друга група крові
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith("second_blood"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    video = os.path.join('assets/video', 'эпик фейл.mp4')

    await state.set_state(Message_State.analis_answer)

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = callback.data

    await state.update_data(quests=quests)

    await callback.message.answer_video(video=FSInputFile(video),
                                            caption="Чи була в одного з батьків, братів\сестер I(О) група крові?",
                                            reply_markup=get_callback_btns(btns={
                                                "Так": "final_yes_blood",
                                                "Ні": "final_no_blood",
                                            }))


@user_private_router.callback_query(Message_State.analis_answer, F.data.startswith('final_yes_blood'))
async def analis_answer(callback: types.CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Так]:"
    quests['gen'] = "[AO,aa]"

    await state.update_data(quests=quests)
   
    await state.clear()


@user_private_router.callback_query(Message_State.analis_answer, F.data.startswith('final_no_blood'))
async def analis_answer_no(callback: types.CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Ні]:"
    quests['gen'] = "[AA,aA]"

    await state.update_data(quests=quests)

    await state.clear()


## Терться група крові
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith("third_blood"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    image =  os.path.join('assets', 'image', 'wqdasd.jpg')

    await state.set_state(Message_State.analis_answer)

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = callback.data

    await state.update_data(quests=quests)
    
    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чи була в одного з батьків, братів\сестер I(О) група крові?",
                                            reply_markup=get_callback_btns(btns={
                                                "Так": "final_yes_blood",
                                                "Ні": "final_no_blood",
                                            }))


@user_private_router.callback_query(Message_State.analis_answer, F.data.startswith('final_yes_blood'))
async def analis_answer(callback: types.CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Так]:"
    quests['gen'] = "[BB,OA]"

    await state.update_data(quests=quests)

    await state.clear()


@user_private_router.callback_query(Message_State.analis_answer, F.data.startswith('final_no_blood'))
async def analis_answer_no(callback: types.CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Ні]:"
    quests['gen'] = "[BO,AO]"

    await state.update_data(quests=quests)

    await state.clear()

## Четверта група крові
@user_private_router.callback_query(Message_State.quest_2, F.data.startswith("fourth_blood"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    # gif = os.path.join('assets', 'image', 'image0-156-1-1.gif')

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = "[IV(AB)]:"
    quests['gen'] = "[AB,OO]"

    await state.update_data(quests=quests)
 
    await state.clear()


# print("Provekra 1")
# @user_private_router.message(Message_State.get_result)
# async def execute_table(message: types.Message, state: FSMContext):
#     print("Provekra 2")
#     male_genotype, children_genotypes, percentage, female_genotype = Punnett_table()
#     print("Provekra 3")
#     await message.answer(text=f"{male_genotype}; \n{female_genotype}; \n{children_genotypes}; \n{percentage}")
    
#     await state.clear()