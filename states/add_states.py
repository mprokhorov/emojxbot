from aiogram.fsm.state import StatesGroup, State


class Add(StatesGroup):
    choosing_image = State()
    choosing_set = State()
    done = State()
