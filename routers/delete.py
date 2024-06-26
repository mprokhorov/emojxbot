from aiogram import Router, Bot, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.inline_keyboard import make_inline_keyboard
from states.delete_states import DeleteSet

router = Router()


@router.message(Command('delete'))
async def cmd_delete(message: Message, state: FSMContext):
    data = await state.get_data()
    sets_list = data['is_empty'].keys()
    if len(sets_list) == 0:
        await message.answer('The list of emoji sets is empty.')
        await state.set_state(DeleteSet.set_deleted)
        return
    await state.set_state(DeleteSet.choosing_set)
    builder = make_inline_keyboard(sets_list)
    delete_list_message = await message.answer('Click on the set you want to delete:', reply_markup=builder.as_markup())
    await state.update_data(chat_id=delete_list_message.chat.id)
    await state.update_data(message_id=delete_list_message.message_id)


@router.callback_query(DeleteSet.choosing_set)
async def delete_set(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    set_name = callback.data
    is_empty = data['is_empty']

    if await bot.delete_sticker_set(set_name):
        is_empty.pop(set_name)
        await state.update_data(is_empty=is_empty)
        await callback.message.reply(f'Emoji set {set_name} was deleted.', reply_markup=ReplyKeyboardRemove())
        await state.set_state(DeleteSet.set_deleted)
        await callback.answer()
    else:
        await callback.message.reply(f'Emoji set {set_name} was not deleted.')
        await callback.answer()

    data = await state.get_data()

    if len(is_empty) == 0:
        await bot.edit_message_text(
            chat_id=data['chat_id'],
            message_id=data['message_id'],
            text='The list of emoji sets is empty.',
            reply_markup=make_inline_keyboard([]).as_markup()
        )
    else:
        builder = make_inline_keyboard(is_empty.keys())
        await bot.edit_message_text(
            chat_id=data['chat_id'],
            message_id=data['message_id'],
            text='Click on the set you want to delete:',
            reply_markup=builder.as_markup()
        )
