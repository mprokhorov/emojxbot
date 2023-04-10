from aiogram.fsm.state import StatesGroup, State


class New(StatesGroup):
    choosing_set_name = State()
    choosing_set_title = State()
    set_created = State()
