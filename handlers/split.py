from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InputSticker, BufferedInputFile
from PIL import Image
from scripts.crop import split_static_image
from keyboards.simple_row import make_row_keyboard

router = Router()


class Split(StatesGroup):
    choosing_image = State()
    choosing_set = State()
    done = State()


@router.message(Command('split'))
async def cmd_split(message: Message, state: FSMContext):
    await message.reply(text='Send one file with extension .png or .jpeg which has height and width divisible by '
                             '100. Number of tiles should not exceed 200.')
    await state.set_state(Split.choosing_image)


@router.message(Split.choosing_image, F.document)
async def get_document(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    document = message.document
    splitted_image = await bot.download(document.file_id)
    await state.update_data(image_to_split=splitted_image)
    await state.set_state(Split.choosing_set)
    keyboard = make_row_keyboard(data['sets_list'])
    await message.reply(text='Now choose emoji set to which emoji tiles will be added.', reply_markup=keyboard)


@router.message(Split.choosing_set)
async def choose_emoji_set(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    set_name = message.text
    if set_name not in data['sets_list']:
        await message.reply('Choose existing set which was created by @emojxbot')
        return
    current_emoji_set = await bot.get_sticker_set(f"{data['chosen_emoji_set_name']}_by_emojxbot")
    sticker_to_delete = current_emoji_set.stickers[0].file_id
    await bot.delete_sticker_from_set(sticker_to_delete)
    image = data['image_to_split']
    img_to_split = Image.open(image)
    tiles_to_add = split_static_image(img_to_split)
    for i, buf in enumerate(tiles_to_add):
        text_file = BufferedInputFile(buf, filename=f"pic{i}.png")
        current_emoji = InputSticker(sticker=text_file, emoji_list=['✂️'])
        await bot.add_sticker_to_set(message.from_user.id, set_name, current_emoji)
    await message.reply("Done!", reply_markup=None)
