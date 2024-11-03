import os

from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message

from keyboard.InlineKeyboard import get_callback_btns
from service.survey_manager import get_survey_filename, get_survey_result

from .first_survey_handlers import *
from .second_survey_handlers import *

from ..MessageState import MessageState
from ..router import user_private_router

from ..constants import SURVEYS_PER_PAGE


# Handler що не буде давати вводити команди під час запуску history
@user_private_router.message(
    StateFilter(MessageState.waiting_for_survey_selection),
    Command("help", "start", "about", "survey"),
)
async def block_commands(message: Message, state: FSMContext):
    current_state = await state.get_state()
    gif = os.path.join("assets", "image", "bot eto da.webm")
    await message.answer_sticker(sticker=FSInputFile(gif), emoji="✋")
    await message.answer(
        "Опа, а низя низя!! Доки не скасуешь history, або не закінчешь роботу з histor низя буде використовувати команди"
    )


## Handlers відповідаючи за history
@user_private_router.message(Command("history"))
async def detailed_survey(message: Message, state: FSMContext):
    user_id = message.from_user.id
    survey_filenames = get_survey_filename(user_id=user_id)
    total_pages = (len(survey_filenames) + SURVEYS_PER_PAGE - 1) // SURVEYS_PER_PAGE
    current_page = 1

    await show_survey_history(
        message, survey_filenames, current_page, total_pages, state
    )


# Handler що показує кількість пройдених опитуваннь
async def show_survey_history(
    message: Message,
    survey_filenames: list,
    current_page: int,
    total_pages: int,
    state: FSMContext,
):
    start_idx = (current_page - 1) * SURVEYS_PER_PAGE
    page_surveys = survey_filenames[start_idx : start_idx + SURVEYS_PER_PAGE]

    history_message = (
        f"📜 Історія опитуваннь (сторінка {current_page}/{total_pages})\n\n"
        + "\n".join([f"✅ {filename}" for filename in page_surveys])
        + "\n\nВиберіть опитування або перейдіть на іншу сторінку:"
    )

    await message.answer(
        history_message,
        reply_markup=get_callback_btns(
            btns={
                "⬅️ Назад": f"page_{current_page - 1}",
                "➡️ Вперед": f"page_{current_page + 1}",
                "❌ Відмінити": "cancel_history",
            }
        ),
    )

    await state.update_data(
        survey_filenames=survey_filenames,
        current_page=current_page,
        total_pages=total_pages,
    )
    await state.set_state(MessageState.waiting_for_survey_selection)


@user_private_router.message(MessageState.waiting_for_survey_selection)
async def proc_survey_selection(message: Message, state: FSMContext):
    user_id = message.from_user.id
    selected_survey = message.text.strip()

    data = await state.get_data()
    survey_filenames = data.get(
        "survey_filenames"
    )  # Забираємо список пройдених опитувань

    survey_id = int(
        selected_survey.split("_")[-1].split(".")[0]
    )  # Забираємо номер опитування
    survey_data = get_survey_result(user_id=user_id, survey_id=survey_id)

    if survey_data:
        results = survey_data["results"]
        results_message = "\n".join(
            [
                f"\t\t\t\t📌 Питання {question_id}: {response if response is not None else 'Не відповіли'}"
                for question_id, response in results.items()
            ]
        )  # Створюємо строку з результатами опитування використовуючи result.items() для перебору та форматування кожного питання та його відповіді

        await message.answer(
            text=(
                f"📄 Деталі опитування №{survey_data['survey_id']}:\n"
                f"👤 ID користувача: {survey_data['user_id']}\n"
                f"📝 Результати:\n{results_message}"
            )
        )
    else:
        await message.answer("Не вдалося отримати данні. Спробуйте пізніше")

    await state.clear()


@user_private_router.callback_query(StateFilter("*"))
async def handle_pagination(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    survey_filenames = data.get("survey_filenames")
    current_page = data.get("current_page")
    total_pages = data.get("total_pages")

    if callback.data.startswith("page_"):
        new_page = int(callback.data.split("_")[1])
        await show_survey_history(
            callback.message, survey_filenames, new_page, total_pages, state
        )

    if callback.data == "cancel_history":
        await cancel_user_history(callback, state)

    await callback.answer()


@user_private_router.callback_query(
    StateFilter("*"), F.data.startswith("cancel_history")
)
async def cancel_user_history(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Історія завершилась, можете використовувати команди")
