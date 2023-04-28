from aiogram.fsm.state import StatesGroup, State


class Forwarded(StatesGroup):
    choosing_image = State()
    done = State()
