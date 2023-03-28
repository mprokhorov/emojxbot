from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InputSticker, Sticker, StickerSet
from aiogram.methods import get_sticker_set

router = Router()

white_png = "BQACAgIAAxkBAAOIZBHOfU5S3Rw1WkZal691TedJT7cAAvIpAAJW7JBI_C6MWrsM7HsvBA"


class NewEmojiSet(StatesGroup):
    choosing_emoji_set_name = State()
    choosing_emoji_set_title = State()
    done = State()


@router.message(Command("new_emoji_set"))
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
    await bot.create_new_sticker_set(message.chat.id, f"{data['chosen_emoji_set_name']}_by_emojxbot",
                                     data['chosen_emoji_set_title'],
                                     [InputSticker(sticker=white_png, emoji_list=['😁'])],
                                     "static", "custom_emoji")
    await message.answer(
        text=f"Emoji set was created successfully! You can find it at: "
             f"t.me/addstickers/{data['chosen_emoji_set_name']}_by_emojxbot"
    )

    current_emoji_set = await bot.get_sticker_set(f"{data['chosen_emoji_set_name']}_by_emojxbot")
    await state.set_state(NewEmojiSet.done)
    # sticker_to_delete = current_emoji_set.stickers[0].file_id
    # await bot.delete_sticker_from_set(sticker_to_delete)


@router.message(NewEmojiSet.choosing_emoji_set_title, ~F.text.regexp(r'^.{1,64}$'))
async def emoji_set_name_title_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer(
        text="Incorrect title"
    )

# @router.message(F.content_type.in_({'document'}))
# async def emoji_image_chosen(message: Message, state: FSMContext):
#     print(message.document.file_id)

# @router.message(NewEmojiSet.choosing_first_emoji_image, F.content_type.in_({'document'}))
# async def emoji_image_chosen(message: Message, state: FSMContext):
#     await message.answer("Now send me 100x100 .png file pls.")
#     await state.update_data(chosen_file_id=message.document.file_id)
#     await state.set_state(NewEmojiSet.choosing_first_emoji_alias)
#
#
# @router.message(NewEmojiSet.choosing_first_emoji_alias, Command("post"))
# async def post_set(message: Message, state: FSMContext, bot: Bot):
#     user_data = await state.get_data()
#     await bot.create_new_sticker_set(message.chat.id, f"{user_data['chosen_emoji_set_name']}_by_emojxbot",
#                                      user_data['chosen_emoji_set_title'],
#                                      [InputSticker(sticker=user_data['chosen_file_id'], emoji_list=['😁', ])],
#                                      "static", "custom_emoji")
#     await message.answer(
#         text=f"Sticker set was created successfully! You can find it at: "
#              f"t.me/addstickers/{user_data['chosen_emoji_set_name']}_by_emojxbot"
#     )
