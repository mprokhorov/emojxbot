from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from keyboards.simple_row import make_row_keyboard

router = Router()


class DeleteSet(StatesGroup):
    choosing_set = State()
    set_deleted = State()


@router.message(Command('delete'))
async def cmd_split(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(DeleteSet.choosing_set)
    keyboard = make_row_keyboard(data['sets_list'])
    await message.reply(text='Now choose emoji set to delete.', reply_markup=keyboard)


@router.message(DeleteSet.choosing_set)
async def cmd_split(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    set_name = message.text
    if set_name not in data['sets_list']:
        await message.reply('Choose existing set which was created by @emojxbot')
        return
    print(await bot.delete_sticker_set(set_name))
    await message.reply(f'Set {set_name} was deleted!')
    await state.set_state(DeleteSet.set_deleted)
