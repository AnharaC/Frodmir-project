from aiogram.fsm.state import StatesGroup, State


class MessageState(StatesGroup):
    quest_1 = State()
    quest_2 = State()
    quest_3 = State()
    analis_answer = State()
