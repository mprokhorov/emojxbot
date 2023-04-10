from aiogram.fsm.state import StatesGroup, State


class DeleteSet(StatesGroup):
    choosing_set = State()
    set_deleted = State()
