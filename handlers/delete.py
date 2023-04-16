from aiogram import Router, Bot, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states.delete_states import DeleteSet

router = Router()


@router.message(Command('delete'))
async def cmd_split(message: Message, state: FSMContext):
    data = await state.get_data()
    sets_list = data['is_empty'].keys()
    await state.set_state(DeleteSet.choosing_set)
    builder = InlineKeyboardBuilder()
    for set_ in sets_list:
        builder.add(InlineKeyboardButton(text=set_, callback_data=set_))
    await message.answer(
        "Choose a set to delete",
        reply_markup=builder.as_markup()
    )
    # keyboard = make_row_keyboard(sets_list)
    # await message.reply(text='Now choose emoji set to delete.', reply_markup=keyboard)


@router.callback_query(DeleteSet.choosing_set)
async def delete_set(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    set_name = callback.data
    is_empty = data['is_empty']
    # sets_list = is_empty.keys()
    # if set_name not in sets_list:
    #     await message.reply('Choose existing set which was created by @emojxbot')
    #     return
    print(set_name)
    was_deleted = await bot.delete_sticker_set(set_name)

    if was_deleted:
        is_empty.pop(set_name)
        await state.update_data(is_empty=is_empty)
        await callback.message.reply(f'Set {set_name} was deleted!', reply_markup=ReplyKeyboardRemove())
        await state.set_state(DeleteSet.set_deleted)
    else:
        await callback.message.reply('Set was not deleted.')
