from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InputSticker, Sticker, StickerSet
from aiogram.methods import get_sticker_set
from PIL import Image
from scripts.crop import split_static_image

router = Router()


class Split(StatesGroup):
    choosing_image = State()
    choosing_set = State()


@router.message(Command('split'))
async def cmd_split(message: Message, state: FSMContext):
    await message.reply(text='Send one file with extension .png or .jpeg which has height and width divisible by '
                             '100. Number of tiles should not exceed 200.')
    await state.set_state(Split.choosing_image)


@router.message(Split.choosing_image, F.document)
async def get_document(message: Message, state: FSMContext, bot: Bot):
    file_id = message.document.file_id
    file_name = message.document.file_name
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, file_name)
    await state.update_data(image_to_split=file_name)
    await message.reply(text='Now choose emoji set to which emoji tiles will be added.')
    await state.set_state(Split.choosing_set)


@router.message(Split.choosing_set, Command('choose_set'))
async def choose_emoji_set(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    image = data['image_to_split']
    img_to_split = Image.open(image)
    split_static_image(img_to_split, f'scripts/out/{image.split(".")[0]}_split', 'png')
