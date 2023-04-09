from aiogram.fsm.state import StatesGroup, State


class Split(StatesGroup):
    choosing_image = State()
    choosing_set = State()
    done = State()
