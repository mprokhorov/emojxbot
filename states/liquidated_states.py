from aiogram.fsm.state import StatesGroup, State


class Liquidated(StatesGroup):
    choosing_image = State()
    done = State()
