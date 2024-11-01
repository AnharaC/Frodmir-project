from aiogram import types, F
import os

from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.types import Message, FSInputFile

from keyboard.InlineKeyboard import get_callback_btns

from service.analysis_data import Punnett_table
from .MessageState import MessageState
from .router import user_private_router

from middleware.MessageMiddleware import UserMessageMiddleware
from middleware.CallbackMiddleware import CallbackMiddleware

user_private_router.message.middleware(UserMessageMiddleware())
user_private_router.callback_query.middleware(CallbackMiddleware())


## Handlers відповідаючи за команди
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


@user_private_router.message(Command("history"))
async def detailed_survey(message: Message):
    photo = os.path.join('assets', 'image', 'photo_2024-10-26_13-10-32.jpg')
    await message.answer_photo(photo=FSInputFile(photo), caption="Резульата опитування N[num_result]: Чоловічий генотип: N; \n"
                 "Жіночий генотип: N; \n"
                 "Дитячі генотипи: N; \n"
                 "Відсотки: N;",
                 reply_markup=get_callback_btns(btns={
                     "Назад": "back",
                     "Далі": "next",
                 }))


@user_private_router.message(StateFilter(None), or_f(Command("survey"), (F.text.lower() == "опитування")))
async def command_start_handler(message: Message, state: FSMContext):
    image = os.path.join('assets', 'image', 'photo_2024-10-16_08-56-42.jpg')

    await state.set_state(MessageState.quest_1)
    await state.update_data(quests={
        "start_quest": {
            "result_quest1": None,
            "result_quest2": None,
            "result_quest3": None
        },
        "gen": {
            1: None,
            2: None
        }
    })

    await message.answer_photo(photo=FSInputFile(image), caption="За якими ознаками ви хотіл би розпочати?",
                                            reply_markup=get_callback_btns(btns={
                                                "Колір очей": "type_of_color_eye",
                                                "Група крові": "type_of_blood",
                                                "Назад": "return",
                                                "Відмінити": "cancel",
                                            }))


## Handlers які відповідальні за "Назад" та "Відмінити"
@user_private_router.callback_query(StateFilter("*"), F.data.startswith("cancel"))
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    curent_state = await state.get_state()
    if curent_state is None:
        return

    await state.clear()
    await callback.message.answer("Опитування була відмінено")


@user_private_router.callback_query(StateFilter("*"), F.data.startswith("return"))
async def back_step_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    user_data = await state.get_data()
    quests = user_data.get('quests', {})

    if current_state == MessageState.quest_1:
        sticker = os.path.join('assets', 'image', 'svabodin.webm')
        await callback.message.answer_sticker(sticker=FSInputFile(sticker), emoji="🤬")
        await callback.message.answer("А все! Нема куди повертатися, анлак бро", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return

    previous_question = quests['start_quest'].get('result_quest1', None)

    await callback.message.answer("Ви повернулись на попередне питання. Зачекайте поки повториться питання")

    if previous_question == 'type_of_color_eye':
        if current_state == MessageState.quest_2.state:
            await command_start_handler(callback.message, state)

        elif current_state == MessageState.quest_3.state:
            await first_quest_eye(callback, state)

        elif current_state == MessageState.analis_answer.state:
            await second_quest_kari(callback, state)

    elif previous_question == 'type_of_blood':
        if current_state == MessageState.quest_2.state:
            await command_start_handler(callback.message, state)

        elif current_state == MessageState.quest_3:
            await first_survey_blood(callback, state),
        
    previous = None
    for step in MessageState.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            return

        previous = step

genotypes = []

## Все про очи
@user_private_router.callback_query(MessageState.quest_1, F.data.startswith('type_of_color_eye'))
async def first_quest_eye(callback: types.CallbackQuery, state: FSMContext):
    gif = os.path.join('assets', 'image', 'аллах-халяль.gif')

    await state.set_state(MessageState.quest_2)

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest1'] = callback.data

    await state.update_data(quests=quests)
    await callback.message.answer_animation(animation=FSInputFile(gif),
                                                reply_markup=get_callback_btns(btns={
                                                    "Блакитні": "blue",
                                                    "Карі": "kari",
                                                    "Зелено/Світло карі": "green/light_brown",
                                                    "Назад": "return",
                                                    "Відмінити": "cancel"
                                                }, sizes=(2,1,2)))
    

## Все про карій
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith('kari'))
async def second_quest_kari(callback: types.CallbackQuery, state: FSMContext):
    image = os.path.join('assets', 'image', 'furry-фэндомы-furry-m-8352840.jpeg')

    await state.set_state(MessageState.quest_3)

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = callback.data

    await state.update_data(quests=quests)
    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чи були в одного з батьків, братів/сестер блакитні очі?",
                                            reply_markup=get_callback_btns(btns={
                                                "Так": "final_yes_kari",
                                                "Ні": "final_no_kari",
                                                "Назад": "return",
                                                "Відмінити": "cancel"
                                            }))
    

@user_private_router.callback_query(MessageState.quest_3, F.data.startswith('final_yes_kari'))
async def analis_answer_yes(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await state.set_state(MessageState.analis_answer)

    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Так]:"
    quests['gen'][1] = "[Aa]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][1])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, перший етап опитування, тобто про генотип першого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до другого етапу": "type_of_color_eye_second",
                                            }))


@user_private_router.callback_query(MessageState.quest_3, F.data.startswith('final_no_kari'))
async def analis_answer_no(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await state.set_state(MessageState.analis_answer)

    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Ні]:"
    quests['gen'][1] = "[AA]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][1])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, перший етап опитування, тобто про генотип першого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до другого етапу": "type_of_color_eye_second",
                                            }))

    

## Все про блакитний
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith('blue'))
async def analis_answer_blue(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = callback.data
    quests['gen'][1] = "[aa]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][1])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, перший етап опитування, тобто про генотип першого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до другого етапу": "type_of_color_eye_second",
                                            }))


    
## Все про світло зелено блакитний
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith('green/light_brown'))
async def analis_answer_green_light_brown(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = "[зелено-блакитні]:"
    quests['gen'][1] = "[Aa]"

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][1])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, перший етап опитування, тобто про генотип першого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до другого етапу": "type_of_color_eye_second",
                                            }))


    
## Все про групу крові
@user_private_router.callback_query(MessageState.quest_1, F.data.startswith('type_of_blood'))
async def first_survey_blood(callback: types.CallbackQuery, state: FSMContext):
    image = os.path.join('assets', 'image', 'photo_2024-10-19_10-02-38.jpg')

    await state.set_state(MessageState.quest_2)

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
                                                "Назад": "return",
                                                "Відмінити": "cancel",
                                            }, sizes=(3,1,2)))
    

## Перша група крові
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith("first_blood"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = "I(O)"
    quests['gen'][1] = "[OO]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][1])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, перший етап опитування, тобто про генотип першого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до другого етапу": "type_of_blood_second",
                                            }))


    


## Друга група крові
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith("second_blood"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    video = os.path.join('assets/video', 'эпик фейл.mp4')

    await state.set_state(MessageState.quest_3)

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = callback.data

    await state.update_data(quests=quests)
    await callback.message.answer_video(video=FSInputFile(video),
                                            caption="Чи була в одного з батьків, братів\сестер I(О) група крові?",
                                            reply_markup=get_callback_btns(btns={
                                                "Так": "final_yes_blood",
                                                "Ні": "final_no_blood",
                                                "Назад": "return",
                                                "Відмінити": "cancel",                                                
                                            }))
    

@user_private_router.callback_query(MessageState.quest_3, F.data.startswith('final_yes_blood'))
async def analis_answer(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await state.set_state(MessageState.analis_answer)

    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Так]:"
    quests['gen'][1] = "[AO]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][1])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, перший етап опитування, тобто про генотип першого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до другого етапу": "type_of_blood_second",
                                            }))


    


@user_private_router.callback_query(MessageState.quest_3, F.data.startswith('final_no_blood'))
async def analis_answer_no(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await state.set_state(analis_answer)

    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Ні]:"
    quests['gen'][1] = "[AA]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][1])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, перший етап опитування, тобто про генотип першого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до другого етапу": "type_of_blood_second",
                                            }))

    


## Терться група крові
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith("third_blood"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    image =  os.path.join('assets', 'image', 'wqdasd.jpg')

    await state.set_state(MessageState.quest_3)

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = callback.data
    
    await state.update_data(quests=quests)

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чи була в одного з батьків, братів\сестер I(О) група крові?",
                                            reply_markup=get_callback_btns(btns={
                                                "Так": "final_yes_blood",
                                                "Ні": "final_no_blood",
                                                "Назад": "return",
                                                "Відмінити": "cancel",                                                
                                            }))
    

@user_private_router.callback_query(MessageState.quest_3, F.data.startswith('final_yes_blood'))
async def analis_answer(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await state.set_state(MessageState.analis_answer)

    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Так]:"
    quests['gen'][1] = "[BO]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][1])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, перший етап опитування, тобто про генотип першого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до другого етапу": "type_of_blood_second",
                                            }))


    
@user_private_router.callback_query(MessageState.quest_3, F.data.startswith('final_no_blood'))
async def analis_answer_no(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await state.set_state(MessageState.analis_answer)

    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Ні]:"
    quests['gen'][1] = "[BB]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][1])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, перший етап опитування, тобто про генотип першого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до другого етапу": "type_of_blood_second",
                                            }))

    
## Четверта група крові
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith("fourth_blood"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = "[IV(AB)]:"
    quests['gen'][1] = "[AB]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][1])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, перший етап опитування, тобто про генотип першого партнера, завершено!)", 
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до другого етапу": "type_of_blood_second",
                                            }))



 # другий етап опитування   - колір очей

@user_private_router.callback_query(MessageState.quest_2, F.data.startswith("type_of_color_eye_second"))
async def second_questionare(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    gif = os.path.join('assets', 'image', 'аллах-халяль.gif')

    await state.set_state(MessageState.quest_2)

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest1'] = callback.data

    await state.update_data(quests=quests)
    await callback.message.answer_animation(animation=FSInputFile(gif),
                                                reply_markup=get_callback_btns(btns={
                                                    "Блакитні": "blue_second",
                                                    "Карі": "kari_second",
                                                    "Зелено/Світло карі": "green/light_brown_second",
                                                    "Назад": "return",
                                                    "Відмінити": "cancel"
                                                }, sizes=(2,1,2)))
    
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith('kari_second'))
async def second_quest_kari(callback: types.CallbackQuery, state: FSMContext):
    image = os.path.join('assets', 'image', 'furry-фэндомы-furry-m-8352840.jpeg')

    await state.set_state(MessageState.quest_3)

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = callback.data

    await state.update_data(quests=quests)
    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чи були в одного з батьків, братів/сестер блакитні очі?",
                                            reply_markup=get_callback_btns(btns={
                                                "Так": "final_yes_kari_second",
                                                "Ні": "final_no_kari_second",
                                                "Назад": "return",
                                                "Відмінити": "cancel"
                                            }))
    

@user_private_router.callback_query(MessageState.quest_3, F.data.startswith('final_yes_kari_second'))
async def analis_answer_yes(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await state.set_state(MessageState.analis_answer)

    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Так]:"
    quests['gen'][2] = "[Aa]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][2])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до результатів": "Pennet_table_results",
                                            }))


@user_private_router.callback_query(MessageState.quest_3, F.data.startswith('final_no_kari_second'))
async def analis_answer_no(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await state.set_state(MessageState.analis_answer)

    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Ні]:"
    quests['gen'][2] = "[AA]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][2])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до результатів": "Pennet_table_results",
                                            }))


@user_private_router.callback_query(MessageState.quest_2, F.data.startswith('blue_second'))
async def analis_answer_blue(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = callback.data
    quests['gen'][2] = "[aa]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][2])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до результатів": "Pennet_table_results",
                                            }))


@user_private_router.callback_query(MessageState.quest_2, F.data.startswith('green/light_brown_second'))
async def analis_answer_green_light_brown(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = "[зелено-блакитні]:"
    quests['gen'][2] = "[Aa]"

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][2])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до результатів": "Pennet_table_results",
                                            }))



     # другий етап опитування   - група крові

@user_private_router.callback_query(MessageState.quest_1, F.data.startswith('type_of_blood_second'))
async def first_survey_blood(callback: types.CallbackQuery, state: FSMContext):
    image = os.path.join('assets', 'image', 'photo_2024-10-19_10-02-38.jpg')

    await state.set_state(MessageState.quest_2)

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest1'] = callback.data
    
    await state.update_data(quests=quests)

    await callback.message.answer_photo(photo=FSInputFile(image), caption="Яка ваша група крові?",
                                            reply_markup=get_callback_btns(btns={
                                                "I(O)": "first_blood_second",
                                                "II(A)": "second_blood_second",
                                                "III(B)": "third_blood_second",
                                                "IV(AB)": "fourth_blood_second",
                                                "Назад": "return",
                                                "Відмінити": "cancel",
                                            }, sizes=(3,1,2)))
    

## Перша група крові
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith("first_blood_second"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = "I(O)"
    quests['gen'][2] = "[OO]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][2])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до результатів": "Pennet_table_results",
                                            }))


## Друга група крові
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith("second_blood_second"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    video = os.path.join('assets/video', 'эпик фейл.mp4')

    await state.set_state(MessageState.quest_3)

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = callback.data

    await state.update_data(quests=quests)
    await callback.message.answer_video(video=FSInputFile(video),
                                            caption="Чи була в одного з батьків, братів\сестер I(О) група крові?",
                                            reply_markup=get_callback_btns(btns={
                                                "Так": "final_yes_blood_second",
                                                "Ні": "final_no_blood_second",
                                                "Назад": "return",
                                                "Відмінити": "cancel",                                                
                                            }))
    

@user_private_router.callback_query(MessageState.quest_3, F.data.startswith('final_yes_blood_second'))
async def analis_answer(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await state.set_state(MessageState.analis_answer)

    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Так]:"
    quests['gen'][2] = "[AO]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][2])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до результатів": "Pennet_table_results",
                                            }))



@user_private_router.callback_query(MessageState.quest_3, F.data.startswith('final_no_blood_second'))
async def analis_answer_no(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await state.set_state(analis_answer)

    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Ні]:"
    quests['gen'][2] = "[AA]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][2])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до результатів": "Pennet_table_results",
                                            }))


## Терться група крові
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith("third_blood_second"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    image =  os.path.join('assets', 'image', 'wqdasd.jpg')

    await state.set_state(MessageState.quest_3)

    user_data = await state.get_data()
    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = callback.data
    
    await state.update_data(quests=quests)

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чи була в одного з батьків, братів\сестер I(О) група крові?",
                                            reply_markup=get_callback_btns(btns={
                                                "Так": "final_yes_blood",
                                                "Ні": "final_no_blood",
                                                "Назад": "return",
                                                "Відмінити": "cancel",                                                
                                            }))
    

@user_private_router.callback_query(MessageState.quest_3, F.data.startswith('final_yes_blood'))
async def analis_answer(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await state.set_state(MessageState.analis_answer)

    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Так]:"
    quests['gen'][2] = "[BO]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][2])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до результатів": "Pennet_table_results",
                                            }))

    
@user_private_router.callback_query(MessageState.quest_3, F.data.startswith('final_no_blood_second'))
async def analis_answer_no(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    await state.set_state(MessageState.analis_answer)

    quests = user_data['quests']
    quests['start_quest']['result_quest3'] = "[Ні]:"
    quests['gen'][2] = "[BB]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][2])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до результатів": "Pennet_table_results",
                                            }))

    
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith("fourth_blood_second"))
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    quests = user_data['quests']
    quests['start_quest']['result_quest2'] = "[IV(AB)]:"
    quests['gen'][2] = "[AB]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()
    genotypes.append(user_data['quests']['gen'][2])

    await callback.message.answer_photo(photo=FSInputFile(image),
                                            caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
                                            reply_markup=get_callback_btns(btns={
                                                "Перейти до результатів": "Pennet_table_results",
                                            }))


# Таблиця Пеннета - окремий хендлер
@user_private_router.callback_query(MessageState.quest_2, F.data.startswith("Pennet_table_results"))
async def first_quest(callback: types.CallbackQuery, message: Message):
    await message.answer(text=(f"{Punnett_table(genotypes)}"))