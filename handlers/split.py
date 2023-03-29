import json
import types

from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InputSticker, Sticker, StickerSet, BufferedInputFile
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.methods import get_sticker_set
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
    # file_id = message.document.file_id
    # file_name = message.document.file_name
    # file = await bot.get_file(file_id)
    # file_path = file.file_path
    # await bot.download_file(file_path, file_name)
    # await state.update_data(image_to_split=file_name)
    # await message.reply(text='Now choose emoji set to which emoji tiles will be added.')
    # await state.set_state(Split.choosing_set)
    data = await state.get_data()
    document = message.document
    splitted_image = await bot.download(document.file_id)
    # await message.reply(text=f'{type(splitted_image)}')
    await state.update_data(image_to_split=splitted_image)
    await state.set_state(Split.choosing_set)
    print(data['sets_list'])
    keyboard = make_row_keyboard(data['sets_list'])
    await message.reply(text='Now choose emoji set to which emoji tiles will be added.', reply_markup=keyboard)


@router.message(Split.choosing_set)
async def choose_emoji_set(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    set_name = message.text
    # if set_name not in data['sets_list']:
    #     message.reply('Choose existing set which was created by @emojxbot')
    #     return
    await message.reply("Started!", reply_markup=ReplyKeyboardRemove())
    image = data['image_to_split']
    img_to_split = Image.open(image)
    tiles_to_add = split_static_image(img_to_split)
    await message.reply(text=len(tiles_to_add))
    for i, buf in enumerate(tiles_to_add):
        text_file = BufferedInputFile(buf, filename=f"pic{i}.png")
        await bot.add_sticker_to_set(message.from_user.id, set_name, InputSticker(sticker=text_file.read(64 * 1024),
                                                                                  emoji_list=['✂️']))
