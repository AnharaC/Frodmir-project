from aiogram.fsm.state import StatesGroup, State

class MessageState(StatesGroup):
    
    waiting_for_survey_selection = State()

    quest_1 = State()
    quest_2 = State()
    quest_3 = State()

    stage_1 = State()
    st_quest_2 = State()
    st_quest_3 = State()
    
    stage_2 = State()