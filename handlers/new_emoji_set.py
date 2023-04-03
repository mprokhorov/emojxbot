from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InputSticker

router = Router()

initilal_emoji_id = "BQACAgIAAxkBAAIDJGQrT-N9j73KpQ_rLoetiPfeAAHzcwACGywAAjE_WEn-ME34KeKPgi8E"


class NewEmojiSet(StatesGroup):
    choosing_emoji_set_name = State()
    choosing_emoji_set_title = State()
    done = State()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(sets_list=[])


@router.message(Command("new"))
async def cmd_new_emoji_set(message: Message, state: FSMContext):
    await state.set_state(NewEmojiSet.choosing_emoji_set_name)
    await message.answer(
        text="Enter name of sticket set, which will be used in t.me/addstickers/ URLs. Can contain only English "
             "letters, digits and underscores. Must begin with a letter, can't contain consecutive underscores. URL "
             "will end in _by_emojxbot. 1-52 characters.")


@router.message(NewEmojiSet.choosing_emoji_set_name, F.text.regexp(r'^[a-zA-Z](?!.*__)[a-zA-Z0-9_]{0,51}$'))
async def emoji_set_name_chosen_correctly(message: Message, state: FSMContext):
    await state.update_data(chosen_emoji_set_name=message.text)
    await state.set_state(NewEmojiSet.choosing_emoji_set_title)
    await message.answer(text="Now choose sticket set title, 1-64 characters")


@router.message(NewEmojiSet.choosing_emoji_set_name, ~F.text.regexp(r'^[a-zA-Z](?!.*__)[a-zA-Z0-9_]{0,51}$'))
async def emoji_set_name_chosen_incorrectly(message: Message):
    await message.answer(text="Incorrect sticker set name. "
                              "Please, make sure your name meets all conditions."
                         )


@router.message(NewEmojiSet.choosing_emoji_set_title, F.text.regexp(r'^.{1,64}$'))
async def emoji_set_name_title_chosen_correctly(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(chosen_emoji_set_title=message.text)
    data = await state.get_data()
    await bot.create_new_sticker_set(message.chat.id, f'{data["chosen_emoji_set_name"]}_by_emojxbot',
                                     data['chosen_emoji_set_title'],
                                     [InputSticker(sticker=initilal_emoji_id, emoji_list=['✂️'])],
                                     'static', 'custom_emoji')
    await message.answer(
        text=f'Emoji set was created successfully! You can find it at: '
             f't.me/addstickers/{data["chosen_emoji_set_name"]}_by_emojxbot'
    )
    sets_list = data['sets_list']
    sets_list.append(f'{data["chosen_emoji_set_name"]}_by_emojxbot')
    await state.update_data(sets_list=sets_list)
    await state.set_state(NewEmojiSet.done)


@router.message(NewEmojiSet.choosing_emoji_set_title, ~F.text.regexp(r'^.{1,64}$'))
async def emoji_set_name_title_chosen_incorrectly(message: Message):
    await message.answer(
        text="Incorrect title"
    )
