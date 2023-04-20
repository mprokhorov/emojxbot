from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputSticker

from config_reader import config
from states.new_states import New

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(is_empty={})


@router.message(Command("new"))
async def cmd_new_emoji_set(message: Message, state: FSMContext):
    await state.set_state(New.choosing_set_name)
    await message.answer(
        text="Enter name of emoji set, which will be used in t.me/addstickers/ URLs. It can contain only English "
             "letters, digits and underscores. It must begin with a letter, can't contain consecutive underscores. URL "
             "will end in _by_emojxbot. It may contain up to 52 characters.")


@router.message(New.choosing_set_name, F.text.regexp(r'^[a-zA-Z](?!.*__)[a-zA-Z0-9_]{0,51}$'))
async def emoji_set_name_chosen_correctly(message: Message, state: FSMContext):
    await state.update_data(chosen_emoji_set_name=message.text)
    await state.set_state(New.choosing_set_title)
    await message.answer(text="Choose title for your emoji set. It may contain up to 64 characters.")


@router.message(New.choosing_set_name, ~F.text.regexp(r'^[a-zA-Z](?!.*__)[a-zA-Z0-9_]{0,51}$'))
async def emoji_set_name_chosen_incorrectly(message: Message):
    await message.answer(text="Incorrect name. "
                              "Please, make sure your name meets all requirements and try again."
                         )


@router.message(New.choosing_set_title, F.text.regexp(r'^.{1,64}$'))
async def emoji_set_name_title_chosen_correctly(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(chosen_emoji_set_title=message.text)
    data = await state.get_data()
    await bot.create_new_sticker_set(message.chat.id, f'{data["chosen_emoji_set_name"]}_by_emojxbot',
                                     data['chosen_emoji_set_title'],
                                     [InputSticker(sticker=config.empty_emoji_id.get_secret_value(),
                                                   emoji_list=['✂️'])], 'static', 'custom_emoji')
    await message.answer(
        text=f'Emoji set was created successfully. You can find it at: '
             f't.me/addstickers/{data["chosen_emoji_set_name"]}_by_emojxbot'
    )
    is_empty = data['is_empty']
    is_empty[f'{data["chosen_emoji_set_name"]}_by_emojxbot'] = True
    await state.update_data(is_empty=is_empty)
    await state.set_state(New.set_created)


@router.message(New.choosing_set_title, ~F.text.regexp(r'^.{1,64}$'))
async def emoji_set_name_title_chosen_incorrectly(message: Message):
    await message.answer(
        text="Incorrect title."
             "Please, make sure your title meets all requirements and try again."
    )
