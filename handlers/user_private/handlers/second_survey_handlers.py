from aiogram import types, F
import os

from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import FSInputFile

from keyboard.InlineKeyboard import get_callback_btns
from service.analysis_data import Punnett_table
from service.survey_manager import save_survey

from ..MessageState import MessageState
from ..router import user_private_router


# Таблиця Пеннета - окремий хендлер
@user_private_router.callback_query(
    MessageState.stage_2, F.data.startswith("Pennet_table_results")
)
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    gen = data.get("quests").get("gen")

    print(gen)

    await Punnett_table(callback, genotypes=gen)


# другий етап опитування - колір очей
@user_private_router.callback_query(
    MessageState.stage_1, F.data.startswith("type_of_color_eye_second")
)
async def second_questionare(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Друге опитування почалося:")

    gif = os.path.join("assets", "image", "аллах-халяль.gif")

    await state.set_state(MessageState.st_quest_2)

    user_data = await state.get_data()
    quests = user_data["quests"]
    quests["start_quest"]["result_quest1"] = callback.data

    await state.update_data(quests=quests)
    await callback.message.answer_animation(
        animation=FSInputFile(gif),
        reply_markup=get_callback_btns(
            btns={
                "Блакитні": "blue_second",
                "Карі": "kari_second",
                "Зелено/Світло карі": "green/light_brown_second",
                "Назад": "return",
                "Відмінити": "cancel",
            },
            sizes=(2, 1, 2),
        ),
    )


@user_private_router.callback_query(
    MessageState.st_quest_2, F.data.startswith("blue_second")
)
async def third_quest_eye(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    image = os.path.join("assets", "image", "gay.webp")

    await state.set_state(MessageState.stage_2)

    quests = user_data["quests"]
    quests["start_quest"]["result_quest2"] = callback.data
    quests["gen"][2] = "[aa]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()

    await callback.message.answer_photo(
        photo=FSInputFile(image),
        caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
        reply_markup=get_callback_btns(
            btns={
                "Перейти до результатів": "Pennet_table_results",
                "Назад": "return",
                "Відмінити": "cancel",
            },
            sizes=(1, 2),
        ),
    )

    # state_data = await state.get_data()
    # user_id = state_data.get("user_id")
    # print(f"Callback user:{user_id}")

    # save_survey(user_id=user_id, )


@user_private_router.callback_query(
    MessageState.st_quest_2, F.data.startswith("kari_second")
)
async def third_quest_eye(callback: types.CallbackQuery, state: FSMContext):
    image = os.path.join("assets", "image", "furry-фэндомы-furry-m-8352840.jpeg")

    await state.set_state(MessageState.st_quest_3)

    user_data = await state.get_data()
    quests = user_data["quests"]
    quests["start_quest"]["result_quest2"] = callback.data

    await state.update_data(quests=quests)
    await callback.message.answer_photo(
        photo=FSInputFile(image),
        caption="Чи були в одного з батьків, братів/сестер блакитні очі?",
        reply_markup=get_callback_btns(
            btns={
                "Так": "final_yes_kari_second",
                "Ні": "final_no_kari_second",
                "Назад": "return",
                "Відмінити": "cancel",
            }
        ),
    )


@user_private_router.callback_query(
    MessageState.st_quest_3, F.data.startswith("final_yes_kari_second")
)
async def st_quest_3_yes(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    image = os.path.join("assets", "image", "hop za aiki.webm")

    await state.set_state(MessageState.stage_2)

    quests = user_data["quests"]
    quests["start_quest"]["result_quest3"] = "[Так]:"
    quests["gen"][2] = "[Aa]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()

    await callback.message.answer_photo(
        photo=FSInputFile(image),
        caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
        reply_markup=get_callback_btns(
            btns={
                "Перейти до результатів": "Pennet_table_results",
                "Назад": "return",
                "Відмінити": "cancel",
            },
            sizes=(1, 2),
        ),
    )

    # state_data = await state.get_data()
    # user_id = state_data.get("user_id")
    # print(f"Callback user:{user_id}")

    # save_survey(user_id=user_id)


@user_private_router.callback_query(
    MessageState.st_quest_3, F.data.startswith("final_no_kari_second")
)
async def st_quest_3_no(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    image = os.path.join("assets", "image", "hehe.webp")

    await state.set_state(MessageState.stage_2)

    quests = user_data["quests"]
    quests["start_quest"]["result_quest3"] = "[Ні]:"
    quests["gen"][2] = "[AA]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()

    await callback.message.answer_photo(
        photo=FSInputFile(image),
        caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
        reply_markup=get_callback_btns(
            btns={
                "Перейти до результатів": "Pennet_table_results",
                "Назад": "return",
                "Відмінити": "cancel",
            },
            sizes=(1, 2),
        ),
    )

    state_data = await state.get_data()
    user_id = state_data.get("user_id")
    print(f"Callback user:{user_id}")

    save_survey(
        user_id=user_id,
    )


@user_private_router.callback_query(
    MessageState.st_quest_2, F.data.startswith("green/light_brown_second")
)
async def st_quest_3_green_light_brown(
    callback: types.CallbackQuery, state: FSMContext
):
    user_data = await state.get_data()
    image = os.path.join("assets", "image", "wow.webp")

    await state.set_state(MessageState.stage_2)

    quests = user_data["quests"]
    quests["start_quest"]["result_quest2"] = "[зелено-блакитні]:"
    quests["gen"][2] = "[Aa]"

    user_data = await state.get_data()

    await callback.message.answer_photo(
        photo=FSInputFile(image),
        caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
        reply_markup=get_callback_btns(
            btns={
                "Перейти до результатів": "Pennet_table_results",
                "Назад": "return",
                "Відмінити": "cancel",
            },
            sizes=(1, 2),
        ),
    )

    # state_data = await state.get_data()
    # user_id = state_data.get("user_id")
    # print(f"Callback user:{user_id}")

    # save_survey(user_id=user_id, )


# другий етап опитування - група крові


@user_private_router.callback_query(
    MessageState.stage_1, F.data.startswith("type_of_blood_second")
)
async def second_quest_blood(callback: types.CallbackQuery, state: FSMContext):
    image = os.path.join("assets", "image", "photo_2024-10-19_10-02-38.jpg")

    await state.set_state(MessageState.st_quest_2)

    user_data = await state.get_data()
    quests = user_data["quests"]
    quests["start_quest"]["result_quest1"] = callback.data

    await state.update_data(quests=quests)

    await callback.message.answer_photo(
        photo=FSInputFile(image),
        caption="Яка ваша група крові?",
        reply_markup=get_callback_btns(
            btns={
                "I(O)": "first_blood_second",
                "II(A)": "second_blood_second",
                "III(B)": "third_blood_second",
                "IV(AB)": "fourth_blood_second",
                "Назад": "return",
                "Відмінити": "cancel",
            },
            sizes=(3, 1, 2),
        ),
    )


## Перша група крові
@user_private_router.callback_query(
    MessageState.st_quest_2, F.data.startswith("first_blood_second")
)
async def first_quest(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    image = os.path.join("assets", "image", "blep.webp")

    await state.set_state(MessageState.stage_2)

    quests = user_data["quests"]
    quests["start_quest"]["result_quest2"] = "I(O)"
    quests["gen"][2] = "[OO]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()

    await callback.message.answer_photo(
        photo=FSInputFile(image),
        caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
        reply_markup=get_callback_btns(
            btns={
                "Перейти до результатів": "Pennet_table_results",
                "Назад": "return",
                "Відмінити": "cancel",
            },
            sizes=(1, 2),
        ),
    )

    # state_data = await state.get_data()
    # user_id = state_data.get("user_id")
    # print(f"Callback user:{user_id}")

    # save_survey(user_id=user_id, )


## Друга група крові
@user_private_router.callback_query(
    MessageState.st_quest_2, F.data.startswith("second_blood_second")
)
async def third_quest_blood(callback: types.CallbackQuery, state: FSMContext):
    video = os.path.join("assets", "video", "эпик фейл.mp4")

    await state.set_state(MessageState.st_quest_3)

    user_data = await state.get_data()
    quests = user_data["quests"]
    quests["start_quest"]["result_quest2"] = callback.data

    await state.update_data(quests=quests)
    await callback.message.answer_video(
        video=FSInputFile(video),
        caption="Чи була в одного з батьків, братів\сестер I(О) група крові?",
        reply_markup=get_callback_btns(
            btns={
                "Так": "final_yes_blood_second_second",
                "Ні": "final_no_blood_second_second",
                "Назад": "return",
                "Відмінити": "cancel",
            }
        ),
    )


@user_private_router.callback_query(
    MessageState.st_quest_3, F.data.startswith("final_yes_blood_second_second")
)
async def st_quest_3(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    gif = os.path.join("assets", "image", "dance.webp")

    await state.set_state(MessageState.stage_2)

    quests = user_data["quests"]
    quests["start_quest"]["result_quest3"] = "[Так]:"
    quests["gen"][2] = "[AO]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()

    await callback.message.answer_photo(
        photo=FSInputFile(gif),
        caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
        reply_markup=get_callback_btns(
            btns={
                "Перейти до результатів": "Pennet_table_results",
                "Назад": "return",
                "Відмінити": "cancel",
            },
            sizes=(1, 2),
        ),
    )

    # state_data = await state.get_data()
    # user_id = state_data.get("user_id")
    # print(f"Callback user:{user_id}")

    # save_survey(user_id=user_id, )


@user_private_router.callback_query(
    MessageState.st_quest_3, F.data.startswith("final_no_blood_second_second")
)
async def st_quest_3_no(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    image = os.path.join("assets", "image", "owo2.webp")

    await state.set_state(MessageState.stage_2)

    quests = user_data["quests"]
    quests["start_quest"]["result_quest3"] = "[Ні]:"
    quests["gen"][2] = "[AA]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()

    await callback.message.answer_photo(
        photo=FSInputFile(image),
        caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
        reply_markup=get_callback_btns(
            btns={
                "Перейти до результатів": "Pennet_table_results",
                "Назад": "return",
                "Відмінити": "cancel",
            },
            sizes=(1, 2),
        ),
    )

    # state_data = await state.get_data()
    # user_id = state_data.get("user_id")
    # print(f"Callback user:{user_id}")

    # save_survey(user_id=user_id, )


## Терться група крові
@user_private_router.callback_query(
    MessageState.st_quest_2, F.data.startswith("third_blood_second")
)
async def third_quest_blood(callback: types.CallbackQuery, state: FSMContext):
    image = os.path.join("assets", "image", "wqdasd.jpg")

    await state.set_state(MessageState.st_quest_3)

    user_data = await state.get_data()
    quests = user_data["quests"]
    quests["start_quest"]["result_quest2"] = callback.data

    await state.update_data(quests=quests)

    await callback.message.answer_photo(
        photo=FSInputFile(image),
        caption="Чи була в одного з батьків, братів\сестер I(О) група крові?",
        reply_markup=get_callback_btns(
            btns={
                "Так": "final_yes_blood_second",
                "Ні": "final_no_blood_second",
                "Назад": "return",
                "Відмінити": "cancel",
            }
        ),
    )


@user_private_router.callback_query(
    MessageState.st_quest_3, F.data.startswith("final_yes_blood_second")
)
async def st_quest_3(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    image = os.path.join("assets", "image", "whof.webp")

    await state.set_state(MessageState.stage_2)

    quests = user_data["quests"]
    quests["start_quest"]["result_quest3"] = "[Так]:"
    quests["gen"][2] = "[BO]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()

    await callback.message.answer_photo(
        photo=FSInputFile(image),
        caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
        reply_markup=get_callback_btns(
            btns={
                "Перейти до результатів": "Pennet_table_results",
                "Назад": "return",
                "Відмінити": "cancel",
            },
            sizes=(1, 2),
        ),
    )

    # state_data = await state.get_data()
    # user_id = state_data.get("user_id")
    # print(f"Callback user:{user_id}")

    # save_survey(user_id=user_id, )


@user_private_router.callback_query(
    MessageState.st_quest_3, F.data.startswith("final_no_blood_second")
)
async def st_quest_3_no(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    image = os.path.join("assets", "image", "gha gha.webp")

    await state.set_state(MessageState.stage_2)

    quests = user_data["quests"]
    quests["start_quest"]["result_quest3"] = "[Ні]:"
    quests["gen"][2] = "[BB]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()

    await callback.message.answer_photo(
        photo=FSInputFile(image),
        caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
        reply_markup=get_callback_btns(
            btns={
                "Перейти до результатів": "Pennet_table_results",
                "Назад": "return",
                "Відмінити": "cancel",
            },
            sizes=(1, 2),
        ),
    )

    # state_data = await state.get_data()
    # user_id = state_data.get("user_id")
    # print(f"Callback user:{user_id}")

    # save_survey(user_id=user_id, )


@user_private_router.callback_query(
    MessageState.st_quest_2, F.data.startswith("fourth_blood_second")
)
async def third_quest_blood(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    image = os.path.join("assets", "image", "wha.webp")

    await state.set_state(MessageState.stage_2)

    quests = user_data["quests"]
    quests["start_quest"]["result_quest2"] = "[IV(AB)]:"
    quests["gen"][2] = "[AB]"

    await state.update_data(quests=quests)

    user_data = await state.get_data()

    await callback.message.answer_photo(
        photo=FSInputFile(image),
        caption="Чудово, другий етап опитування, тобто про генотип другого партнера, завершено!)",
        reply_markup=get_callback_btns(
            btns={
                "Перейти до результатів": "Pennet_table_results",
                "Назад": "return",
                "Відмінити": "cancel",
            },
            sizes=(1, 2),
        ),
    )

    # state_data = await state.get_data()
    # user_id = state_data.get("user_id")
    # print(f"Callback user:{user_id}")

    # save_survey(user_id=user_id, )
