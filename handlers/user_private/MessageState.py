from aiogram.fsm.state import StatesGroup, State

class MessageState(StatesGroup):
    # start_quest = State()
    quest_1 = State()
    quest_2 = State()
    quest_3 = State()
    analis_answer = State()