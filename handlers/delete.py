from aiogram import Router, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from states.delete_states import DeleteSet

router = Router()


@router.message(Command('delete'))
async def cmd_split(message: Message, state: FSMContext):
    data = await state.get_data()
    sets_list = data['is_empty'].keys()
    await state.set_state(DeleteSet.choosing_set)
    keyboard = make_row_keyboard(sets_list)
    await message.reply(text='Now choose emoji set to delete.', reply_markup=keyboard)


@router.message(DeleteSet.choosing_set)
async def cmd_split(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    set_name = message.text
    is_empty = data['is_empty']
    sets_list = is_empty.keys()
    if set_name not in sets_list:
        await message.reply('Choose existing set which was created by @emojxbot')
        return
    if await bot.delete_sticker_set(set_name):
        is_empty.pop(set_name)
        await state.update_data(is_empty=is_empty)
        await message.reply(f'Set {set_name} was deleted!', reply_markup=ReplyKeyboardRemove())
        await state.set_state(DeleteSet.set_deleted)
    else:
        await message.reply('Set was not deleted.')
